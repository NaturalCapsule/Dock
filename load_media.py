import urllib.request
import gi
import hashlib
import urllib
import os

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import GLib, Gdk, GdkPixbuf
from media import MediaPlayerMonitor
import cairo

media = MediaPlayerMonitor()

title_name, player_name = '', ''


def create_radius_pixbuf(pixbuf):
    width, height = pixbuf.get_width(), pixbuf.get_height()

    corner_radius = 30

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    ctx.set_source_rgba(0, 0, 0, 0)
    ctx.set_operator(cairo.Operator.SOURCE)
    ctx.paint()

    ctx.set_operator(cairo.Operator.OVER)
    ctx.move_to(corner_radius, 0)
    ctx.line_to(width - corner_radius, 0)
    ctx.arc(width - corner_radius, corner_radius, corner_radius, 3 * 3.1416 / 2, 2 * 3.1416)
    ctx.line_to(width, height - corner_radius)
    ctx.arc(width - corner_radius, height - corner_radius, corner_radius, 0, 3.1416 / 2)
    ctx.line_to(corner_radius, height)
    ctx.arc(corner_radius, height - corner_radius, corner_radius, 3.1416 / 2, 3.1416)
    ctx.line_to(0, corner_radius)
    ctx.arc(corner_radius, corner_radius, corner_radius, 3.1416, 3 * 3.1416 / 2)
    ctx.close_path()

    bite_radius = corner_radius // 2  
    bite_angle_start = 1.5 
    bite_angle_end = 2.0   

    ctx.arc(corner_radius, corner_radius, bite_radius, bite_angle_start * 3.1416, bite_angle_end * 3.1416)
    ctx.line_to(corner_radius, corner_radius)

    ctx.clip()

    gdk_cairo = Gdk.cairo_surface_create_from_pixbuf(pixbuf, 0, None)
    ctx.set_source_surface(gdk_cairo, 0, 0)

    ctx.paint()

    return Gdk.pixbuf_get_from_surface(surface, 0, 0, width, height)


def safe_set_label(label, text):
    GLib.idle_add(label.set_text, text)

def safe_set_image(image_widget, pixbuf):
    GLib.idle_add(image_widget.set_from_pixbuf, pixbuf)

def get_cached_filename(title):
    hashed = hashlib.md5(title.encode()).hexdigest()
    return f"/tmp/{hashed}.jpg"


def update_media(label, image):
    global title_name, player_name
    media.monitor()
    thumbnail = None
    
    current_player = media.current_player or ''
    current_title = media.title_ or ''
    should_update = False

    if player_name != current_player:
        print(f"Player changed: {player_name} → {current_player}")
        player_name = current_player
        should_update = True

    if title_name != current_title:
        print(f"Title changed: {title_name} → {current_title}")
        title_name = current_title
        should_update = True

    if current_player:
        try:
            if should_update:
                print(f"title: {current_title}\nartist: {media.artist}")
                
                current_title = str(current_title)
                if len(current_title) >= 8:
                    current_title = f'{current_title[:8]}...'
                
                safe_set_label(label, current_title)
                
                height, width = 90, 90
                if 'file:///' in media.art_url:
                    thumbnail = media.art_url.replace('file:///', '/')
                    height, width = 90, 90
                elif 'https://' in media.art_url or 'http://' in media.art_url:
                    thumbnail = get_cached_filename(current_title)
                    if not os.path.exists(thumbnail):
                        print(f"Downloading thumbnail to cache: {thumbnail}")
                        urllib.request.urlretrieve(media.art_url, thumbnail)
                    else:
                        print(f"Using cached thumbnail: {thumbnail}")
                    height, width = 55, 70

                if thumbnail and os.path.exists(thumbnail):
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(thumbnail, width, height)
                    radius_pixbuf = create_radius_pixbuf(pixbuf)

                    print("Setting images safely...")
                    safe_set_image(image, radius_pixbuf)
                    image.show()



        except Exception as e:
            print(f"Exception in update_image: {e}")

    else:
        safe_set_label(label, '')
        image.hide()

    return True


# def update_media(title_label, image):
#     global title_name, player_name
#     media.monitor()
#     thumbnail = None
    
#     current_player = media.current_player or ''
#     current_title = media.title_ or ''
#     should_update = False

#     if player_name != current_player:
#         print(f"Player changed: {player_name} → {current_player}")
#         player_name = current_player
#         should_update = True

#     if title_name != current_title:
#         print(f"Title changed: {title_name} → {current_title}")
#         title_name = current_title
#         should_update = True

#     if current_player:
#         try:
#             if should_update:
#                 print(f"title: {current_title}\nartist: {media.artist}")

#                 safe_set_label(title_label, current_title)
                
#                 media_ = f'{current_title}'
#                 height, width = 90, 90
#                 if 'file:///' in media.art_url:
#                     thumbnail = media.art_url.replace('file:///', '/')
#                     height, width = 90, 90
#                 elif 'https://' in media.art_url or 'http://' in media.art_url:
#                     thumbnail = get_cached_filename(current_title)
#                     if not os.path.exists(thumbnail):
#                         print(f"Downloading thumbnail to cache: {thumbnail}")
#                         urllib.request.urlretrieve(media.art_url, thumbnail)
#                     else:
#                         print(f"Using cached thumbnail: {thumbnail}")
#                     height, width = 50, 100

#                 if thumbnail and os.path.exists(thumbnail):
#                     pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(thumbnail, height, width)
#                     circular_pixbuf = create_radius_pixbuf(pixbuf)
#                     # print(type(media_))
#                     if len(media_) >= 8:
#                         media_ = f"{media_[:8]}..."
#                     print("Setting images safely...")
#                     safe_set_image(image, circular_pixbuf)
#                     safe_set_label(title_label, media_)
#                     image.show()


#         except Exception as e:
#             print(f"Exception in update_image: {e}")

#     else:
#         safe_set_label(title_label, '')
#         image.hide()

#     return True


def update_pauseplay(button):
    if not media.current_player or media.playback_status == 'Paused':
        button.set_label('')
        
    elif media.playback_status == 'Playing':
        button.set_label('')


    return True

//
// main.vala - part of likebox-player
//
// Copyright (C) 2011 Michael Budde <mbudde@gmail.com>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//

public class Likebox.Main : GLib.Object {

    static bool debug_mode;
    [CCode (array_length = false, array_null_terminated = true)]
    static string[] filenames;

    private const OptionEntry[] options = {
        { "debug", 'd', 0, OptionArg.NONE, ref debug_mode, "Print debug messages" },
        { "", 0, 0, OptionArg.FILENAME_ARRAY, ref filenames, null, "FILE" },
        { null }
    };

    public static int main (string[] args) {
        var context = new OptionContext ("");
        context.add_main_entries (options, null);
        try {
            context.parse (ref args);
        } catch (OptionError e) {
            printerr (e.message);
            printerr ("\n");
            return 1;
        }

        if (!debug_mode) {
            Log.set_default_handler ((d, l, m) => {});
        }

        var collection = new TrackCollection ("likebox.db");
        if (filenames != null) {
            // Load tracks in database
            foreach (var filename in filenames) {
                string uri;
                try {
                    uri = Filename.to_uri (filename);
                } catch (ConvertError e) {
                    warning (e.message);
                    continue;
                }
                var file = new TagLib.File (filename);
                var track = new TrackInfo ();
                track.uri = uri;
                track.artist = file.tag.artist;
                track.album = file.tag.album;
                track.title = file.tag.title;
                track.year = file.tag.year;
                collection.save_track (track);
                message ("saved track \"%s\"", track.title);
            }
        } else {
            var tracks = collection.get_all_tracks ();
            if (tracks.size == 0) {
                printerr ("No tracks found. Aborting.\n");
                return 1;
            }
            play_tracks (args, tracks);
        }
        return 0;
    }

    public static void play_tracks (string[] args, Gee.List<TrackInfo> tracks) {
        var engine = new PlayerEngine (args);
        var mainloop = new MainLoop ();

        engine.player_event.connect ((s, e) => {
                switch (e) {
                case PlayerEngine.Event.START_OF_STREAM:
                    message ("started playing \"%s\"", engine.current_track.title);
                    break;
                case PlayerEngine.Event.STATE_CHANGE:
                    if (engine.current_state == PlayerEngine.State.IDLE) {
                        if (tracks.size > 0) {
                            var track = tracks.remove_at (0);
                            engine.open_track (track);
                            engine.play ();
                        } else {
                            message ("no more tracks to play");
                            mainloop.quit ();
                        }
                    } else {
                        debug ("new state: %s", engine.current_state.to_string ());
                    }
                    break;
                }
                stdout.flush ();
            });

        var track = tracks.remove_at (0);
        engine.open_track (track);
        engine.play ();
        mainloop.run ();
    }

    public static void log_handler (string? log_domain, LogLevelFlags log_levels, string message) {
        printerr (message);
        printerr ("\n");
    }

}

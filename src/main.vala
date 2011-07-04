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
        context.parse (ref args);

        if (filenames == null) {
            printerr ("Missing filename\n");
            return 1;
        }

        if (!debug_mode) {
            Log.set_default_handler ((d, l, m) => {});
        }

        var engine = new PlayerEngine (args);
        var mainloop = new MainLoop ();

        engine.player_event.connect ((s, e) => {
                debug (@"player event: $e");
                switch (e) {
                case PlayerEngine.Event.END_OF_STREAM:
                    mainloop.quit ();
                    break;
                case PlayerEngine.Event.VOLUME:
                    debug ("volume: %u", engine.volume);
                    break;
                case PlayerEngine.Event.STATE_CHANGE:
                    debug ("state change: %s", engine.current_state.to_string ());
                    break;
                }
                stdout.flush ();
            });


        var uri = Filename.to_uri (filenames[0]);
        var track = new UnknownTrackInfo (uri);
        engine.open_track (track);
        engine.play ();
        mainloop.run ();
        return 0;
    }

    public static void log_handler (string? log_domain, LogLevelFlags log_levels, string message) {
        printerr (message);
        printerr ("\n");
    }

}

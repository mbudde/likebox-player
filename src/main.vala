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

    public static int main(string[] args) {
        var engine = new PlayerEngine (args);
        var mainloop = new MainLoop ();

        Log.set_handler (null, LogLevelFlags.LEVEL_WARNING | LogLevelFlags.FLAG_FATAL
                   | LogLevelFlags.FLAG_RECURSION, log_handler);

        engine.player_event.connect((s, e) => {
                switch (e) {
                case PlayerEngine.Event.END_OF_STREAM:
                    mainloop.quit ();
                    break;
                case PlayerEngine.Event.VOLUME:
                    stdout.printf ("volume: %u\n", engine.volume);
                    break;
                case PlayerEngine.Event.STATE_CHANGE:
                    stdout.printf("state change: %s\n", engine.current_state.to_string());
                    break;
                }
                stdout.flush ();
            });

        if (args.length <= 1) {
            stdout.printf("Missing filename\n");
            return 1;
        }

        var uri = Filename.to_uri (args[1]);
        var track = new UnknownTrackInfo (uri);
        engine.open_track (track);
        engine.play ();
        mainloop.run ();
        return 0;
    }

    public static void log_handler (string? log_domain, LogLevelFlags log_levels, string message) {
        stderr.printf (message);
    }

}

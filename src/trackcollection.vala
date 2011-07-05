//
// trackcollection.vala - part of likebox-player
//
// Copyright (C) 2011 Michael Budde <mbuddegmail.com>
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

public class Likebox.TrackCollection : GLib.Object {

    private Gee.HashMap<int, TrackInfo> track_cache;
    private Sqlite.Database database;

    public TrackCollection (string location) {
        track_cache = new Gee.HashMap<int, TrackInfo> (null, null);
        Sqlite.Database.open_v2 (location, out database);
        initialize_database ();
    }

    public Gee.List<TrackInfo> get_tracks (int[] track_ids) {
        var tracks = new Gee.ArrayList<TrackInfo> ();
        var not_loaded = new Gee.ArrayList<int> ();
        TrackInfo track;
        foreach (var id in track_ids) {
            track = track_cache[id];
            if (track == null) {
                not_loaded.add (id);
            } else {
                tracks.add (track);
            }
        }
        load_tracks (not_loaded);
        foreach (var id in not_loaded) {
            track = track_cache[id];
            if (track != null) {
                tracks.add (track);
            }
        }
        return tracks;
    }

    public Gee.List<TrackInfo> get_all_tracks () {
        var track_ids = new Gee.ArrayList<int> ();
        Sqlite.Statement stmt;
        string sql;
        sql = "SELECT TrackID FROM Tracks";
        database.prepare_v2 (sql, -1, out stmt);
        int rc = 0;
        do {
            rc = stmt.step ();
            switch (rc) {
            case Sqlite.DONE:
                break;
            case Sqlite.ROW:
                track_ids.add (stmt.column_int (0));
                break;
            default:
                error ("database error: %d, %s", rc, database.errmsg ());
            }
        } while (rc == Sqlite.ROW);
        return get_tracks ((int[])track_ids.to_array ());
    }

    public void save_track (TrackInfo track) {
        Sqlite.Statement stmt;
        string sql;
        if (track.id == 0) {
            sql = "SELECT TrackID FROM Tracks WHERE uri = ?";
            database.prepare_v2 (sql, -1, out stmt);
            stmt.bind_text (1, track.uri);
            int rc = stmt.step ();
            if (rc == Sqlite.ROW) {
                track.id = stmt.column_int (0);
            } else if (rc == Sqlite.DONE) {
                stmt = null;
                sql = "SELECT MAX(TrackID) + 1 FROM Tracks";
                database.prepare_v2 (sql, -1, out stmt);
                if (stmt.step () == Sqlite.ROW) {
                    track.id = stmt.column_int (0);
                    if (track.id == 0)
                        track.id = 1;
                    debug ("setting track id to %d", track.id);
                } else {
                    error ("database error: %d, %s", database.errcode (), database.errmsg ());
                }
            } else {
                error ("database error: %d, %s", database.errcode (), database.errmsg ());
            }
            stmt = null;
        }
        sql = """
            INSERT OR REPLACE INTO Tracks (TrackId, Uri, Artist, Album, Title, Year)
            VALUES (?, ?, ?, ?, ?, ?)
        """;
        database.prepare_v2 (sql, -1, out stmt);
        stmt.bind_int (1, track.id);
        stmt.bind_text (2, track.uri);
        stmt.bind_text (3, track.artist);
        stmt.bind_text (4, track.album);
        stmt.bind_text (5, track.title);
        stmt.bind_int (6, (int)track.year);
        if (stmt.step () != Sqlite.DONE) {
            error ("database error: %d, %s", database.errcode (), database.errmsg ());
        }            
    }

    private void initialize_database () {
        Sqlite.Statement stmt;
        string sql;

        sql = """
            CREATE TABLE Tracks (
                TrackID             INTEGER PRIMARY KEY,
                Uri                 TEXT,
                FileSize            INTEGER,
                Artist              TEXT,
                Album               TEXT,
                Title               TEXT,
                TrackNumber         INTEGER,
                TrackCount          INTEGER,
                Duration            INTEGER,
                Year                INTEGER,
                Genre               TEXT
            );
            CREATE TABLE Playlists (
                PrimarySourceID     INTEGER,
                PlaylistID          INTEGER PRIMARY KEY,
                Name                TEXT,
            );
            CREATE TABLE PlaylistEntries (
                EntryID             INTEGER PRIMARY KEY,
                PlaylistID          INTEGER NOT NULL,
                TrackID             INTEGER NOT NULL,
            );
        """;
        database.prepare_v2 (sql, -1, out stmt);
        return_if_fail (stmt.step () != Sqlite.ROW);
    }

    private void load_tracks (Gee.List<int> track_ids) {
        Sqlite.Statement stmt;
        var id_strings = new string[track_ids.size];
        for (int i = 0; i < track_ids.size; i++) {
            id_strings[i] = track_ids[i].to_string ();
        }
        string sql = """
            SELECT TrackID, Uri, Artist, Album, Title
            FROM Tracks WHERE TrackID IN (%s)
        """.printf (string.joinv (", ", id_strings));
        database.prepare_v2 (sql, -1, out stmt);
        int rc = 0;
        do {
            rc = stmt.step ();
            switch (rc) {
            case Sqlite.DONE:
                break;
            case Sqlite.ROW:
                var track = new TrackInfo ();
                track.id = stmt.column_int (0);
                track.uri = stmt.column_text (1);
                track.artist = stmt.column_text (2);
                track.album = stmt.column_text (3);
                track.title = stmt.column_text (4);
                track_cache[track.id] = track;
                debug ("track %s created", track.title);
                break;
            default:
                error ("database error: %d, %s", rc, database.errmsg ());
            }
        } while (rc == Sqlite.ROW);
    }

}

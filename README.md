jsonwatch — like watch -d but for JSON
======================================

[![Build Status](https://travis-ci.org/dbohdan/jsonwatch.svg?branch=master)](https://travis-ci.org/dbohdan/jsonwatch)

`jsonwatch` is a command line utility with which you can track changes in JSON data delivered by a shell command or a web (HTTP/HTTPS) API. `jsonwatch` requests data from the designated source repeatedly at a set interval and displays the differences when the data changes.  It is similar but not isomorphic in its behavior to how [watch(1)](https://manpages.debian.org/stable/procps/watch.1.en.html) with the `-d` switch works for plain-text data.

It has been tested on Debian 10, Ubuntu 18.04, and Windows 7.

The two previous versions of `jsonwatch` are preserved in the branch [`python`](https://github.com/dbohdan/jsonwatch/tree/python) and [`haskell`](https://github.com/dbohdan/jsonwatch/tree/haskell).


Installation
============

Prebuilt Linux and Windows binaries are available.  They are attached to releases on the [Releases](https://github.com/dbohdan/jsonwatch/releases) page.

Building on Debian and Ubuntu
-----------------------------

Follow the instructions to build a static Linux binary of `jsonwatch` from source on recent Debian and Ubuntu.

1\. Install [Rustup](https://rustup.rs/).  Through Rustup add the stable MUSL target for your CPU.

```sh
rustup target add x86_64-unknown-linux-musl
```

2\. Install the build and testing dependencies.

```sh
sudo apt install build-essential expect musl-tools tcl
```

3\. Clone this repository.  Build and install the binary.

    git clone https://github.com/dbohdan/jsonwatch
    cd jsonwatch
    make test
    make release
    sudo make install "BUILD_USER=$USER"

Cross-compiling for Windows
---------------------------

Follow the instructions to build a 32-bit Windows binary of `jsonwatch` on recent Debian and Ubuntu.

1\. Install [Rustup](https://rustup.rs/).  Through Rustup add the i686 GNU ABI Windows target.

```sh
rustup target add i686-pc-windows-gnu
```

2\. Install the build dependencies.

```sh
sudo apt install build-essential mingw-w64
```

3\. Configure Cargo for cross-compilation.  Put the following in `~/.cargo/config`.

```toml
[target.i686-pc-windows-gnu]
linker = "/usr/bin/i686-w64-mingw32-gcc"
```

4\. Fix the [`crt2.o` issue](https://github.com/rust-lang/rust/issues/48272#issuecomment-429596397).

```sh
cd ~/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/rustlib/i686-pc-windows-gnu/lib/
mv crt2.o crt2.o.bak
cp /usr/i686-w64-mingw32/lib/crt2.o .
```

5\. Clone this repository.  Build the binary.

    git clone https://github.com/dbohdan/jsonwatch
    cd jsonwatch
    make release TARGET=i686-pc-windows-gnu
    cp "/tmp/$USER/jsonwatch-rust/i686-pc-windows-gnu/release/jsonwatch.exe" .


Use examples
============

Commands
--------

### *nix

Testing `jsonwatch`.

    $ jsonwatch -n 1 -c "echo '{ \"filename\": \"'\$(mktemp -u)'\"}'"

    {
        "filename": "/tmp/tmp.ZYFQ5RwGN5"
    }
    2014-03-16T22:40:08.130170 .filename: /tmp/tmp.ZYFQ5RwGN5 -> /tmp/tmp.Pi0WXp2Aoj
    2014-03-16T22:40:09.133995 .filename: /tmp/tmp.Pi0WXp2Aoj -> /tmp/tmp.2U181cBL2L
    2014-03-16T22:40:10.137640 .filename: /tmp/tmp.2U181cBL2L -> /tmp/tmp.i5sGwYig4S
    2014-03-16T22:40:11.141320 .filename: /tmp/tmp.i5sGwYig4S -> /tmp/tmp.Sv0s60LuoT
    2014-03-16T22:40:12.144990 .filename: /tmp/tmp.Sv0s60LuoT -> /tmp/tmp.skSIruBLfQ

Cryptocurrency daemon information (including balance changes).

    $ jsonwatch --no-initial-values -c "dogecoind getinfo"

    2014-03-18T14:16:57.855226 .blocks: 145779 -> 145780
    2014-03-18T14:17:07.922137
        .blocks: 145780 -> 145781
        .difficulty: 1316.42722979 -> 1178.89009968
    2014-03-18T14:19:13.921734 .connections: 8 -> 7
    2014-03-18T14:19:39.128119 .connections: 7 -> 8

### Windows

On Windows `-c` executes `cmd.exe` commands.

    > jsonwatch -c "type test\weather1.json"

    {"clouds": {"all": 92}, "name": "Kiev", "coord": {
    "lat": 50.43, "lon": 30.52}, "sys": {"country": "UA",
    "message": 0.0051, "sunset": 1394985874, "sunrise": 1394942901
    }, "weather": [{"main": "Snow", "id": 612, "icon": "13d",
    "description": "light shower sleet"}, {"main": "Rain", "id":
    520, "icon": "09d", "description": "light intensity shower rain"}],
    "rain": {"3h": 2}, "base": "cmc stations", "dt":
    1394979003, "main": {"pressure": 974.8229, "humidity": 91,
    "temp_max": 277.45, "temp": 276.45, "temp_min": 276.15}, "id"
    : 703448, "wind": {"speed": 10.27, "deg": 245.507}, "cod":
    200}

    2017-03-02T16:58:08+0200 + .test: true
    2017-03-02T17:00:52+0200 .test: true -> false
    2017-03-02T17:01:04+0200 - .test: false

URLs
----

Watching a URL works identically on *nix and on Windows.

Weather tracking.

    $ jsonwatch -u http://api.openweathermap.org/data/2.5/weather\?q\=Kiev,ua --no-initial-values -n 300

    2014-03-17T23:06:19.073790
        + .rain.1h: 0.76
        - .rain.3h: 0.5
        .dt: 1395086402 -> 1395089402
        .main.temp: 279.07 -> 278.66
        .main.temp_max: 279.82 -> 280.15
        .main.temp_min: 277.95 -> 276.05
        .sys.message: 0.0353 -> 0.0083

Geolocation. (Try this on a mobile device.)

    $ jsonwatch -u https://ipinfo.io/ --no-initial-values -n 300


License
=======

`jsonwatch` is distributed under the MIT license.  See the file `LICENSE` for details.   [Wapp](tests/vendor/wapp/wapp.tcl) is copyright (c) 2017 D. Richard Hipp and is distributed under the Simplified BSD License.

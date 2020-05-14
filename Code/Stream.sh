#! /bin/sh

nohup mjpg_streamer -i "input_uvc.so -r 1024x768 -f 30 -y -q 10" --output "output_http.so -w /usr/local/share/mjpg-streamer/www --port 8080"&
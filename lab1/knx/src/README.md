 How to use (python3 knxnetP.py -h to see the usage):

 To write a value:
   python3 knxnetP.py -gwip 127.0.0.1 -gwprt 3671 -a w -v 200 -gadr 3/4/11

 To read a value:
   python3 knxnetP.py -gwip 127.0.0.1 -gwprt 3671 -a r -gadr 4/4/11

 Arguments:
   -gwip/--gateway_ip: Gateway ip
   -gwprt/--gateway_port: Gateway port
   -a/--action: "r" to read, "w" to write
   -v/--value: used only if it is a write action, not required if it is a read action.
               Accept an int value
   -gadr/--group_address: Group Address in form x/y/z

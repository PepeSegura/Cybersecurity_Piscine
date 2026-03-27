objdump -M intel -d level1

<pre>
123c:       e8 ff fd ff ff          call   1040 <strcmp@plt>
1241:       83 f8 00                cmp    eax,0x0
1244:       0f 85 16 00 00 00       jne    1260 <main+0xa0>
124a:       8b 5d 80                mov    ebx,DWORD PTR [ebp-0x80]
124d:       <font color="red">8d 83 2c e0 ff ff</font>       lea    eax,[ebx-0x1fd4]             -> Address of string "Good Job"
1253:       89 04 24                mov    DWORD PTR [esp],eax
1256:       e8 05 fe ff ff          call   1060 <printf@plt>
125b:       e9 11 00 00 00          jmp    1271 <main+0xb1>
1260:       8b 5d 80                mov    ebx,DWORD PTR [ebp-0x80]
1263:       <font color="red">8d 83 37 e0 ff ff</font>       lea    eax,[ebx-0x1fc9]             -> Address of string "Nope"
1269:       89 04 24                mov    DWORD PTR [esp],eax
126c:       e8 ef fd ff ff          call   1060 <printf@plt>
</pre>

I willl modify the address of the string to print.

xxd level1 > level1.hex

Locate the hex values for the string addresses

<pre>
000011e0: 8b83 08e0 ffff 8945 868b 830c e0ff ff89  .......E........
000011f0: 458a 8b83 10e0 ffff 8945 8e66 8b83 14e0  E........E.f....
00001200: ffff 6689 4592 8d83 16e0 ffff 8904 24e8  ..f.E.........$.
00001210: 4cfe ffff 8b5d 808d 4594 8d8b 29e0 ffff  L....]..E...)...
00001220: 890c 2489 4424 04e8 44fe ffff 8b5d 808d  ..$.D$..D....]..
00001230: 4d94 8d55 8689 e089 5004 8908 e8ff fdff  M..U....P.......
00001240: ff83 f800 0f85 1600 0000 8b5d 80<font color="red">8d 832c</font>  ...........]..., -> Address "Good Job"
00001250: <font color="red">e0ff ff</font>89 0424 e805 feff ffe9 1100 0000  .....$..........
00001260: 8b5d 80<font color="red">8d 8337 e0ff ff</font>89 0424 e8ef fdff  .]...7.....$.... -> Address "Nope"
00001270: ff31 c081 c484 0000 005b 5dc3 f30f 1efb  .1.......[].....
00001280: 5383 ec08 e837 feff ff81 c377 2d00 0083  S....7.....w-...
00001290: c408 5bc3 0000 0000 0000 0000 0000 0000  ..[.............
000012a0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
000012b0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
</pre>

Modify this line

> 00001260: 8b5d 808d 83<font color="red">37</font> e0ff ff89 0424 e8ef fdff  .]...7.....$....

to be like this

> 00001260: 8b5d 808d 83<font color="red">2c</font> e0ff ff89 0424 e8ef fdff  .]...7.....$....


xxd -r level1.hex > new_level1
chmod +x new_level1

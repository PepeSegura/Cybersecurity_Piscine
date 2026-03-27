objdump -M intel -d level2

<pre>
000012a0 &lt;ok&gt;:
    12a0:       55                      push   ebp
    12a1:       89 e5                   mov    ebp,esp
    12a3:       53                      push   ebx
    12a4:       50                      push   eax
    12a5:       e8 00 00 00 00          call   12aa &lt;ok+0xa&gt;
    12aa:       5b                      pop    ebx
    12ab:       81 c3 56 5d 00 00       add    ebx,0x5d56
    12b1:       8d 83 <font color="red">11 bd</font> ff ff       lea    eax,[ebx-0x42ef] -&gt; Address string "Good Job"
    12b7:       89 04 24                mov    DWORD PTR [esp],eax
    12ba:       e8 c1 fd ff ff          call   1080 &lt;puts@plt&gt;
    12bf:       83 c4 04                add    esp,0x4
    12c2:       5b                      pop    ebx
    12c3:       5d                      pop    ebp
    12c4:       c3                      ret    
    12c5:       90                      nop
</pre>

<pre>
00001220 &lt;no&gt;:
    1220:	55                   	push   ebp
    1221:	89 e5                	mov    ebp,esp
    1223:	53                   	push   ebx
    1224:	83 ec 14             	sub    esp,0x14
    1227:	e8 00 00 00 00       	call   122c &lt;no+0xc&gt;
    122c:	5b                   	pop    ebx
    122d:	81 c3 d4 5d 00 00    	add    ebx,0x5dd4
    1233:	89 5d f8             	mov    DWORD PTR [ebp-0x8],ebx
    1236:	8d 83 <font color="red">08 b0</font> ff ff    	lea    eax,[ebx-0x4ff8]
    123c:	89 04 24             	mov    DWORD PTR [esp],eax
    123f:	e8 3c fe ff ff       	call   1080 &lt;puts@plt&gt;
    1244:	8b 5d f8             	mov    ebx,DWORD PTR [ebp-0x8]
    1247:	c7 04 24 01 00 00 00 	mov    DWORD PTR [esp],0x1
    124e:	e8 3d fe ff ff       	call   1090 &lt;exit@plt&gt;
    1253:	90                   	nop
    1254:	90                   	nop
    1255:	90                   	nop
</pre>

I willl modify the address of the string to print.

xxd level2 > level2.hex

Locate the hex values for the string addresses

<pre>
000011f0: 0000 e8e9 feff ff83 c410 e831 ffff ffc6  ...........1....
00001200: 833c 0000 0001 8b5d fcc9 c38d 7426 0090  .<.....]....t&..
00001210: f30f 1efb e957 ffff ff8b 1424 c366 9090  .....W.....$.f..
00001220: 5589 e553 83ec 14e8 0000 0000 5b81 c3d4  U..S........[...
00001230: 5d00 0089 5df8 8d83 <font color="red">08b0</font> ffff 8904 24e8  ]...].........$. -> Address string "Nope"
00001240: 3cfe ffff 8b5d f8c7 0424 0100 0000 e83d  <....]...$.....=
00001250: feff ff90 9090 9090 9090 9090 9090 9090  ................
00001260: 5589 e553 83ec 14e8 0000 0000 5b81 c394  U..S........[...
00001270: 5d00 0089 5df8 8d83 0eb0 ffff 8904 24e8  ]...].........$.
00001280: fcfd ffff 8b5d f88d 83cc baff ff89 0424  .....].........$
</pre>

Modify this line

> 00001230: 5d00 0089 5df8 8d83 <font color="red">08b0</font> ffff 8904 24e8  ]...].........$.

to be like this

> 00001230: 5d00 0089 5df8 8d83 <font color="red">11bd</font> ffff 8904 24e8  ]...].........$.


xxd -r level2.hex > new_level2
chmod +x new_level2

Replace the call ___syscall_malloc with noop

    1369:	b8 32 00 00 00       	mov    eax,0x32
    136e:	39 c8                	cmp    eax,ecx
    1370:	0f 84 05 00 00 00    	je     137b <main+0x5b>
    1376:	e8 65 ff ff ff       	call   12e0 <___syscall_malloc>
    137b:	0f be 4d c0          	movsx  ecx,BYTE PTR [rbp-0x40]
    137f:	b8 34 00 00 00       	mov    eax,0x34
    1384:	39 c8                	cmp    eax,ecx
    1386:	0f 84 05 00 00 00    	je     1391 <main+0x71>
    138c:	e8 4f ff ff ff       	call   12e0 <___syscall_malloc>


    1369:	b8 32 00 00 00       	mov    eax,0x32
    136e:	39 c8                	cmp    eax,ecx
    1370:	0f 84 05 00 00 00    	je     137b <main+0x5b>
    1376:	90 90 90 90 90       	call   12e0 <___syscall_malloc>
    137b:	0f be 4d c0          	movsx  ecx,BYTE PTR [rbp-0x40]
    137f:	b8 34 00 00 00       	mov    eax,0x34
    1384:	39 c8                	cmp    eax,ecx
    1386:	0f 84 05 00 00 00    	je     1391 <main+0x71>
    138c:	90 90 90 90 90       	call   12e0 <___syscall_malloc>



I will replace the call to strcmp with xor rax,rax and fill with noop.

    1465:	c6 44 05 df 00       	mov    BYTE PTR [rbp+rax*1-0x21],0x0
    146a:	48 8d 35 93 0b 00 00 	lea    rsi,[rip+0xb93]        # 2004 <_IO_stdin_used+0x4>
    1471:	48 8d 7d df          	lea    rdi,[rbp-0x21]
    1475:	e8 f6 fb ff ff       	call   1070 <strcmp@plt>
    147a:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
    147d:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
    1480:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax


    1465:	c6 44 05 df 00       	mov    BYTE PTR [rbp+rax*1-0x21],0x0
    146a:	48 8d 35 93 0b 00 00 	lea    rsi,[rip+0xb93]        # 2004 <_IO_stdin_used+0x4>
    1471:	48 8d 7d df          	lea    rdi,[rbp-0x21]
    1475:	31 c0 90 90 90       	call   1070 <strcmp@plt>
    147a:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
    147d:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
    1480:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax

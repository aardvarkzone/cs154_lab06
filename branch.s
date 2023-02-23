# cs154 lab6
# All Rights Reserved
# Copyright (c) 2022 University of California Santa Barbara
# Distribution Prohibited

.text
main:
        beq     $0, $0, here1
no1:
        nop
        nop
        addi    $v0, $0, 0xbad  # bad
here1:
        addi    $t0, $0, 0xff
        nop
        nop
        beq     $t0, $0, no2
here2:
        nop
        nop
        addi    $t1, $0, 0xff
        nop
        nop
        beq     $t0, $t1, here3
no2:
no3:
        nop
        nop
        addi    $v0, $0, 0xbad  # bad
here3:
        nop
        nop
        addi    $t2, $0, 0xff
done:
        nop
        nop
        addi    $v1, $0, -1   # done

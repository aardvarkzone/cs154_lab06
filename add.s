# cs154 lab6
# All Rights Reserved
# Copyright (c) 2022 University of California Santa Barbara
# Distribution Prohibited

.text
main:
        addi    $t0, $0, 1      # 1
        nop
        nop
        addi    $t0, $t0, 1     # 2
        nop
        nop
        add     $t0, $t0, $t0   # 4
        nop
        nop
        add     $t0, $t0, $t0   # 8
        nop
        nop
        addi    $t0, $t0, 1     # 9
        nop
        nop
        add     $t0, $t0, $t0   # 18
        nop
        nop
        addi    $t0, $t0, 1     # 19

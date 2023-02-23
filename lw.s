# cs154 lab6
# All Rights Reserved
# Copyright (c) 2022 University of California Santa Barbara
# Distribution Prohibited

.text
main:
        # addi    $t0, $0, 1      # r[t0] := 1
        # sw      $t0, 0($t0)     # m[r[t0]=1] := r[t0] = 1
        # lw      $t1, 0($t0)     # r[t1] := m[r[t0]=1] = 1
        # addi    $t1, $t1, 1     # r[t1]++

        addi    $t1, $0, 1      # r[t1] := 1
        addi    $t2, $0, 2      # r[t2] := 2
        addi    $t3, $0, 3      # r[t3] := 3
        nop
        sw      $t2, 0($t1)     # m[r[t1]=1] := r[t2] = 2
        nop
        nop
        lw      $t1, 0($t1)     # r[t1] := m[r[t1]=1] = 2
        nop
        nop
        sw      $t1, 0($t3)     # m[r[t3]=3] := r[t1] = 2

        addi    $v0, $0, 0xff   # done

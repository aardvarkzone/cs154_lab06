# cs154 lab6
# All Rights Reserved
# Copyright (c) 2022 University of California Santa Barbara
# Distribution Prohibited

.text
main:
        addi    $5, $0, 5
        addi    $3, $0, 3
        addi    $11, $0, 1
        nop
        nop
        nop
        sw      $11, 0($11)
        sw      $3, 0($3)
        sw      $5, 0($5)

        addi    $4, $0, 4       # 4 away
        addi    $2, $0, 2       # 2 away
        nop
        nop
        nop
        sw      $2, 0($2)
        sw      $4, 0($4)

# Testing all instuctions in the instruction set

.text
main:
    # ADD (checking for result in $t0)
    addi $a0, $zero, 1337
    add $t0, $zero, $a0
    add $t0, $t0, $t0
    # $t0 = 2674

    # ADDI (checking for result in $t1)
    addi $a0, $zero, 69
    addi $t1, $a0, 420
    # $t1 = 489

    # AND (checking for result in $t2)
    addi $a0, $zero, 21
    addi $a1, $zero, 42
    and $t2, $t2, $a0
    and $t2, $t2, $a1
    # $t2 = 0
    
    # LUI (checking for result in $t3)
    lui $t3, 5005
    addi $t3, $t3, 5005
    # $t3 = 328012685

    # ORI (checking for result in $t4)
    lui $t4, 6000
    ori $t4, $zero, 789
    ori $t4, $t4, 123
    # $t4 = 895

    # SLT (checking for result in $t5)
    addi $a0, $zero, 22
    addi $a1, $zero, 21
    slt $t5, $a0, $a1
    # $t5 = 0

    # SW (checking for result in $t6)
    addi $a0, $zero, 1000
    addi $a1, $zero, 1337
    sw $a1, -4($sp)
    lw $t6, -4($sp)
    # $t6 = 1337

    # LW (checking for result in $t7)
    sw $a0, -8($sp)
    lw $t7, -8($sp)
    # $t7 = 1000

    # BEQ (loop through exit, checking for result in $v0)
exit:
    addi $v0, $zero, 10
    beq $zero, $zero, exit
    # $v0 = 10
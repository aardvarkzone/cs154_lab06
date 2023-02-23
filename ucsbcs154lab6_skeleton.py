# ucsbcs154lab6
# All Rights Reserved
# Copyright (c) 2022 University of California Santa Barbara
# Distribution Prohibited

import pyrtl


def ucsbcs154lab6_alu(a, b, ALU_op):
    # Based on the given 'op', return the proper signals as outputs
    ALU_out = pyrtl.WireVector(bitwidth=32)
    with pyrtl.conditional_assignment:
        with ALU_op == pyrtl.Const(0x0):
            # ADD
            ALU_out |= a + b
        with ALU_op == pyrtl.Const(0x1):
            # AND
            ALU_out |= a & b
        with ALU_op == pyrtl.Const(0x2):
            # OR
            ALU_out |= a | b
        with ALU_op == pyrtl.Const(0x3):
            # SLT
            ALU_out |= pyrtl.signed_lt(a, b)
        with ALU_op == pyrtl.Const(0x4):
            # SUB
            ALU_out |= a - b
        with ALU_op == pyrtl.Const(0x5):
            # LU
            ALU_out |= pyrtl.concat(b, pyrtl.Const(0, bitwidth=16))

    zero = (ALU_out == 0)

    return ALU_out, zero


def ucsbcs154lab6_control(op, func):
    # ADD, AND, ADDI, LUI, ORI, SLT, LW, SW, BEQ
    control_out = pyrtl.WireVector(bitwidth=10, name='control_out')
    with pyrtl.conditional_assignment:
        with op == pyrtl.Const(0x0):
            with func == pyrtl.Const(0x20):
                # ADD
                control_out |= pyrtl.Const(0x280)
            with func == pyrtl.Const(0x24):
                # AND
                control_out |= pyrtl.Const(0x281)
            with func == pyrtl.Const(0x2A):
                # SLT
                control_out |= pyrtl.Const(0x283)
        with op == pyrtl.Const(0x8):
            # ADDI
            control_out |= pyrtl.Const(0x0A0)
        with op == pyrtl.Const(0xF):
            # LUI
            control_out |= pyrtl.Const(0x0A5)
        with op == pyrtl.Const(0xD):
            # ORI
            control_out |= pyrtl.Const(0x0C2)
        with op == pyrtl.Const(0x23):
            # LW
            control_out |= pyrtl.Const(0x0A8)
        with op == pyrtl.Const(0x2B):
            # SW
            control_out |= pyrtl.Const(0x030)
        with op == pyrtl.Const(0x4):
            # BEQ
            control_out |= pyrtl.Const(0x104)

    reg_dest = control_out[9]
    branch = control_out[8]
    reg_write = control_out[7]
    ALU_src = control_out[5:7]
    mem_write = control_out[4]
    mem_to_reg = control_out[3]
    ALU_op = control_out[:3]

    return reg_dest, branch, reg_write, ALU_src, mem_write, mem_to_reg, ALU_op


# registers/memory
rf = pyrtl.MemBlock(bitwidth=32, addrwidth=32, name='rf', max_read_ports=3, asynchronous=True)
i_mem = pyrtl.MemBlock(bitwidth=32, addrwidth=32, name='i_mem', asynchronous=True)
d_mem = pyrtl.MemBlock(bitwidth=32, addrwidth=32, name='d_mem', asynchronous=True)

pc = pyrtl.Register(bitwidth=32, name='pc', reset_value=(2**32)-4)

instr_fd = pyrtl.Register(bitwidth=32, name='instr_fd')
pc_plus_4_fd = pyrtl.Register(bitwidth=32, name='pc_plus_4_fd')

ALU_op_dx = pyrtl.Register(bitwidth=3, name='ALU_op_dx')
branch_offset_dx = pyrtl.Register(bitwidth=32, name='branch_offset_dx')
pc_plus_4_dx = pyrtl.Register(bitwidth=32, name='pc_plus_4_dx')
branch_dx = pyrtl.Register(bitwidth=1, name='branch_dx')
rf_data_1_dx = pyrtl.Register(bitwidth=32, name='rf_data_1_dx')
rf_data_2_dx = pyrtl.Register(bitwidth=32, name='rf_data_2_dx')
imm_zero_dx = pyrtl.Register(bitwidth=32, name='imm_zero_dx')
imm_sign_dx = pyrtl.Register(bitwidth=32, name='imm_sign_dx')
ALU_src_dx = pyrtl.Register(bitwidth=2, name='ALU_src_dx')
mem_write_dx = pyrtl.Register(bitwidth=1, name='mem_write_dx')
mem_to_reg_dx = pyrtl.Register(bitwidth=1, name='mem_to_reg_dx')
reg_write_dx = pyrtl.Register(bitwidth=1, name='reg_write_dx')
reg_dest_dx = pyrtl.Register(bitwidth=1, name='reg_dest_dx')
rd_dx = pyrtl.Register(bitwidth=32, name='rd_dx')
rt_dx = pyrtl.Register(bitwidth=32, name='rt_dx')

branch_pc_xm = pyrtl.Register(bitwidth=32, name='branch_pc_xm')
to_branch_xm = pyrtl.Register(bitwidth=1, name='to_branch_xm')
ALU_result_xm = pyrtl.Register(bitwidth=32, name='ALU_result_xm')
mem_write_xm = pyrtl.Register(bitwidth=1, name='mem_write_xm')
mem_to_reg_xm = pyrtl.Register(bitwidth=1, name='mem_to_reg_xm')
reg_write_xm = pyrtl.Register(bitwidth=1, name='reg_write_xm')
rd_xm = pyrtl.Register(bitwidth=32, name='rd_xm')
rf_data_2_xm = pyrtl.Register(bitwidth=32, name='rf_data_2_xm')

mem_to_reg_mw = pyrtl.Register(bitwidth=1, name='mem_to_reg_mw')
reg_write_mw = pyrtl.Register(bitwidth=1, name='reg_write_mw')
rd_mw = pyrtl.Register(bitwidth=32, name='rd_mw')
d_mem_read_mw = pyrtl.Register(bitwidth=32, name='d_mem_read_mw')
ALU_result_mw = pyrtl.Register(bitwidth=32, name='ALU_result_mw')


# hazard signals
stall = pyrtl.WireVector(bitwidth=1, name='stall')
to_branch_x = pyrtl.WireVector(bitwidth=1, name='to_branch_x')
rd_x = pyrtl.WireVector(bitwidth=32, name='rd_x')


# fetch
pc_next = pyrtl.WireVector(bitwidth=32, name='pc_next')
with pyrtl.conditional_assignment:
    with stall:
        pc_next |= pc
    with to_branch_xm:
        pc_next |= branch_pc_xm
    with pyrtl.otherwise:
        pc_next |= pc + 4

instr_f = i_mem[pc_next[2:]]
instr_f.name = 'instr_f'


# fetch -> decode
pc.next <<= pc_next
pc_plus_4_fd.next <<= pc_next + 4
instr_fd.next <<= instr_f


# decode
op_d = instr_fd[26:]
rs_d = instr_fd[21:26]
rt_d = instr_fd[16:21]
rd_d = instr_fd[11:16]
sh_d = instr_fd[6:11]
func_d = instr_fd[:6]
imm_d = instr_fd[:16]

reg_dest_d, branch_d, reg_write_d, ALU_src_d, mem_write_d, mem_to_reg_d, ALU_op_d = \
    ucsbcs154lab6_control(op_d, func_d)

  # extra logic because pyrtl mem writes are always posedge synchronous
rf_write_data_w = pyrtl.WireVector(bitwidth=32, name='rf_write_data_w')
rf_write_enable_w = pyrtl.WireVector(bitwidth=1)
wrote_rs_d = rf_write_enable_w & (rs_d==rd_mw)
wrote_rt_d = rf_write_enable_w & (rt_d==rd_mw)
rf_data_1_d = pyrtl.select(wrote_rs_d, rf_write_data_w, rf[rs_d])
rf_data_2_d = pyrtl.select(wrote_rt_d, rf_write_data_w, rf[rt_d])

imm_zero_d = imm_d.zero_extended(bitwidth=32)
imm_sign_d = imm_d.sign_extended(bitwidth=32)

branch_offset_d = pyrtl.shift_left_arithmetic(imm_sign_d, 2)


# hazard
    # stall if execute has LW, and decode has hazard
stall <<= mem_to_reg_dx & (rd_x!=0) & ((rs_d==rd_x) | (rt_d==rd_x))
    # flush "d->x stage" on stalls and branch miss
flush_dx_stage = stall | to_branch_x | to_branch_xm


# decode -> execute
with pyrtl.conditional_assignment:
    with flush_dx_stage:
        rf_data_1_dx.next |= 0
        rf_data_2_dx.next |= 0
        imm_zero_dx.next |= 0
        imm_sign_dx.next |= 0
        ALU_op_dx.next |= 0
        branch_offset_dx.next |= 0
        pc_plus_4_dx.next |= 0
        branch_dx.next |= 0
        ALU_src_dx.next |= 0
        mem_write_dx.next |= 0
        mem_to_reg_dx.next |= 0
        reg_write_dx.next |= 0
        reg_dest_dx.next |= 0
        rd_dx.next |= 0
        rt_dx.next |= 0
    with pyrtl.otherwise:
        rf_data_1_dx.next |= rf_data_1_d
        rf_data_2_dx.next |= rf_data_2_d
        imm_zero_dx.next |= imm_zero_d
        imm_sign_dx.next |= imm_sign_d
        ALU_op_dx.next |= ALU_op_d
        branch_offset_dx.next |= branch_offset_d
        pc_plus_4_dx.next |= pc_plus_4_fd
        branch_dx.next |= branch_d
        ALU_src_dx.next |= ALU_src_d
        mem_write_dx.next |= mem_write_d
        mem_to_reg_dx.next |= mem_to_reg_d
        reg_write_dx.next |= reg_write_d
        reg_dest_dx.next |= reg_dest_d
        rd_dx.next |= rd_d
        rt_dx.next |= rt_d


# execute
    # pass rt into rd if I type
rd_x <<= pyrtl.select(reg_dest_dx, rd_dx, rt_dx)

rf_data_1_x = pyrtl.WireVector(bitwidth=32)
rf_data_1_x <<= rf_data_1_dx

rf_data_2_x = pyrtl.WireVector(bitwidth=32)
rf_data_2_x <<= rf_data_2_dx

ALU_first_x = rf_data_1_x
ALU_first_x.name = 'ALU_first_x'

ALU_second_x = pyrtl.WireVector(bitwidth=32, name='ALU_second_x')
with pyrtl.conditional_assignment:
    with ALU_src_dx==0:
        ALU_second_x |= rf_data_2_x
    with ALU_src_dx==1:
        ALU_second_x |= imm_sign_dx
    with ALU_src_dx==2:
        ALU_second_x |= imm_zero_dx

ALU_result_x, ALU_zero_x = ucsbcs154lab6_alu(ALU_first_x, ALU_second_x, ALU_op_dx)
branch_ALU_result_x = pyrtl.signed_add(pc_plus_4_dx, branch_offset_dx)
to_branch_x <<= branch_dx & ALU_zero_x


# execute -> memory
ALU_result_xm.next <<= ALU_result_x
branch_pc_xm.next <<= branch_ALU_result_x
to_branch_xm.next <<= to_branch_x
mem_write_xm.next <<= mem_write_dx
mem_to_reg_xm.next <<= mem_to_reg_dx
reg_write_xm.next <<= reg_write_dx
rd_xm.next <<= rd_x
rf_data_2_xm.next <<= rf_data_2_x


# memory
d_mem_address_m = pyrtl.shift_left_arithmetic(ALU_result_xm, 2)
d_mem_read_m = d_mem[d_mem_address_m[2:]]
d_mem[d_mem_address_m[2:]] <<= pyrtl.MemBlock.EnabledWrite(rf_data_2_xm, mem_write_xm)


# memory -> writeback
mem_to_reg_mw.next <<= mem_to_reg_xm
reg_write_mw.next <<= reg_write_xm
rd_mw.next <<= rd_xm
d_mem_read_mw.next <<= d_mem_read_m
ALU_result_mw.next <<= ALU_result_xm


# writeback
with pyrtl.conditional_assignment:
    with mem_to_reg_mw:
        rf_write_data_w |= d_mem_read_mw
    with pyrtl.otherwise:
        rf_write_data_w |= ALU_result_mw

rf_write_enable_w <<= (rd_mw!=0) & reg_write_mw
rf[rd_mw] <<= pyrtl.MemBlock.EnabledWrite(rf_write_data_w, rf_write_enable_w)



##################### SIMULATION #####################

if __name__ == '__main__':

    # Start a simulation trace
    ucsbcs154lab6_sim_trace = pyrtl.SimulationTrace()

    # Initialize the i_mem with your instructions.
    i_mem_init = {}
    with open('i_mem_init.txt', 'r') as fin:
        i = 0
        for line in fin.readlines():
            i_mem_init[i] = int(line, 16)
            i += 1

    sim = pyrtl.Simulation(tracer=ucsbcs154lab6_sim_trace, memory_value_map={
        i_mem: i_mem_init
    })

    # Run for an arbitrarily large number of cycles.
    for cycle in range(50):
        sim.step({})

    # Use render_trace() to debug if your code doesn't work.
    # ucsbcs154lab6_sim_trace.render_trace(symbol_len=20)
    # ucsbcs154lab6_sim_trace.print_vcd(open('dump.vcd', 'w'), include_clock=True)

    # You can also print out the register file or memory like so if you want to debug:
    print('mem',sim.inspect_mem(d_mem))
    print('rf',sim.inspect_mem(rf))

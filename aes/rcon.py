from myhdl import block, Signal, always

R_CONSTANTS = ( 0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000,0x20000000, 0x40000000, 0x80000000, 0x1b000000, 0x36000000, 0x00000000)

@block
def rcon_lut(clk, rcon, key_load, R_CONSTANTS):
	addr  = Signal(0)
	
	@always(clk.posedge)
	def logic():
		if (key_load):
			rcon.next = 0x01000000
		else:
			rcon.next = R_CONSTANTS[int(addr)]
	@always(clk.posedge)
	def counter():
		if (key_load):
			addr.next = 0
		else:
			addr.next = addr + 1

	return logic, counter


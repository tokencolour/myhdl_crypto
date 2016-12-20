from myhdl import block, Signal, always
rdict = {	0 : 0x01000000,
			1 : 0x02000000,
			2 : 0x04000000,
			3 : 0x08000000,
			4 : 0x10000000,
			5 : 0x20000000,
			6 : 0x40000000,
			7 : 0x80000000,
			8 : 0x1b000000,
			9 : 0x36000000,
			10 : 0x00000000 }

@block
def rcon_lut(clk, rcon, key_load):
	i  = Signal(0)
	
	@always(clk.posedge)
	def logic():
		if (key_load):
			rcon.next = 0x01000000
		else:
			rcon.next = rdict[int(i)]
	@always(clk.posedge)
	def counter():
		if (key_load):
			i.next = 0
		else:
			i.next = i + 1

	return logic, counter


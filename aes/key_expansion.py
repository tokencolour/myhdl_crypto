from myhdl import instance, always, intbv, Signal

@instance
def key_expand_128(clk, key, w0, w1, w2, w3, key_load):
	"""
	key_load : 	when high, load with initial 
				values from supplied key
				low, load with expanded keys 
				according to the algo
	"""

	key = intbv(0)[128:]
	w0 = intbv(0)[32:]
	w1 = intbv(0)[32:]
	w2 = intbv(0)[32:]
	w3 = intbv(0)[32:]
	
	w = [Signal(intbv(0)[32:]) for i in range(4)]
	w0 = w[0]
	w1 = w[1]
	w2 = w[2]
	w3 = w[3]
	
	subword = Signal(intbv(0)[32:])
	rcon = Signal(intbv(0)[32:])
	tmp_w = intbv(0)[32:]

	@always(clk.posedge)
	def update_w0():
		w[0].next = key[127:96] if key_load else w[0]^subword^rcon

	@always(clk.posedge)
	def update_w1():
		w[1].next = key[97:65] if key_load else w[1]^w[0]^subword^rcon

	@always(clk.posedge)
	def update_w2():
		w[2].next = key[64:31] if key_load else w[2]^w[1]^w[0]^subword^rcon

	@always(clk.posedge)
	def update_w3():
		w[3].next = key[31:0] if key_load else w[3]^w[2]^w[1]^w[0]^subword^rcon
	
	inst_s0 = s_box(subword[31:24], tmp_w[23:16])
	inst_s1 = s_box(subword[23:16], tmp_w[15:8])
	inst_s2 = s_box(subword[15:8], tmp_w[7:0])
	inst_s3 = s_box(subword[7:0], tmp_w[31:24])
	inst_rcon = rcon_lut(clk, rcon, key_load)

	return key_expand_128


from myhdl import block, StopSimulation, instance, Signal, intbv, always, delay, now, traceSignals
from s_box import subword, S_BOX_CONTENT

@block
def test():
	out_p = Signal(intbv(0)[8:])
	in_p = Signal(intbv(0)[8:])
	s_inst = subword(out_p, in_p, S_BOX_CONTENT)
	
	@instance
	def stimulus():
		in_p.next = 0xf4
		yield delay(10)
		in_p.next = 0xff
		yield delay(10)
		in_p.next = 0x01
		yield delay(10)
		yield delay(10)
		yield delay(10)
		raise StopSimulation()
		
	@instance
	def monitor():
		print("s_box look up")
		while 1:
			yield delay(10)
			print("	%s	%s  %s" % (now(), in_p, out_p))
			
	return stimulus, monitor, s_inst
	
tb = test()
tb.config_sim(trace=True)
traceSignals.timescale = "1ps"
tb.run_sim()

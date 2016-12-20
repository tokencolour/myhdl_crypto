from myhdl import block, StopSimulation, instance, Signal, intbv, always, delay, now, traceSignals
from rcon import rcon_lut, R_CONSTANTS
@block
def test():
	clk = Signal(0)
	rcon = Signal(intbv(0)[32:])
	key_load = Signal(0)
	rcon_inst = rcon_lut(clk, rcon, key_load, R_CONSTANTS)

	@always(delay(10))
	def clkgen():
		clk.next = not clk
	
	@instance
	def stimulus():
		key_load.next = 1;
		#yield clk.negedge
		key_load.next = 0;
		for i in range(10):
			yield clk.negedge
		yield delay(20)
		raise StopSimulation()

	@instance
	def monitor():
		print ("rcon_entries")
		while 1:
			yield clk.posedge
			print("	%s	%s" % (now(), rcon))
	return clkgen, stimulus, rcon_inst, monitor

tb = test()
tb.config_sim(trace=True)
traceSignals.timescale = "1ps"
#tb = traceSignals(test)
tb.run_sim()

			

from __future__ import absolute_import
from __future__ import print_function
import sys
import os

# the next line can be removed after installation
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from veriloggen import *
import veriloggen.thread as vthread


def mkLed():
    m = Module('blinkled')
    clk = m.Input('CLK')
    rst = m.Input('RST')

    datawidth = 32
    addrwidth = 10
    numports = 1
    initvals = [i * 0.5 + 10 for i in range(2 ** addrwidth - 100)]
    myram = vthread.FixedRAM(m, 'myram', clk, rst, datawidth, addrwidth,
                             point=8, numports=numports, initvals=initvals)

    def blink(times):
        for i in range(times):
            rdata = myram.read(i)
            print('rdata = %f' % rdata)

        for i in range(times):
            rdata = myram.read(i)

            b = vthread.fixed.FixedConst(0.25, 8)
            wdata = rdata + b
            myram.write(i, wdata)
            print('wdata = %f' % wdata)

        sum = vthread.fixed.FixedConst(0, 8)
        for i in range(times):
            rdata = myram.read(i)
            print('rdata = %f' % rdata)
            sum += rdata

        print('sum = %f' % sum)

    th = vthread.Thread(m, 'th_blink', clk, rst, blink)
    fsm = th.start(10)

    return m


def mkTest():
    m = Module('test')

    # target instance
    led = mkLed()

    # copy paras and ports
    params = m.copy_params(led)
    ports = m.copy_sim_ports(led)

    clk = ports['CLK']
    rst = ports['RST']

    uut = m.Instance(led, 'uut',
                     params=m.connect_params(led),
                     ports=m.connect_ports(led))

    simulation.setup_waveform(m, uut)
    simulation.setup_clock(m, clk, hperiod=5)
    init = simulation.setup_reset(m, rst, m.make_reset(), period=100)

    init.add(
        Delay(10000),
        Systask('finish'),
    )

    return m


if __name__ == '__main__':
    test = mkTest()
    verilog = test.to_verilog('tmp.v')
    print(verilog)

    sim = simulation.Simulator(test)
    rslt = sim.run()
    print(rslt)
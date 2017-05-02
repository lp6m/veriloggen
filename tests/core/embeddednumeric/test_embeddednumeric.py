from __future__ import absolute_import
from __future__ import print_function
import veriloggen
import embeddednumeric

expected_verilog = """

module blinkled #
(
  parameter WIDTH = 8
)
(
  input CLK,
  input RST,
  output reg [WIDTH-1:0] LED
);

  reg [32-1:0] count;

  always @(posedge CLK) begin
    if(RST) begin
      count <= 0;
    end else begin
      if(count == 1023) begin
        count <= 0;
      end else begin
        count <= count + 1;
      end
    end
  end


  always @(posedge CLK) begin
    if(RST) begin
      LED <= 0;
    end else begin
      if(count == 1023) begin
        LED <= LED + 1;
      end 
    end
  end


endmodule

"""


def test():
    veriloggen.reset()
    test_module = embeddednumeric.mkLed()
    code = test_module.to_verilog()

    from pyverilog.vparser.parser import VerilogParser
    from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
    #parser = VerilogParser()
    #expected_ast = parser.parse(expected_verilog)
    #codegen = ASTCodeGenerator()
    #expected_code = codegen.visit(expected_ast)
    expected_code = expected_verilog

    assert(expected_code == code)

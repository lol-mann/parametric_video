from manimlib.imports import *
import numpy as np
from gtts import gTTS
import manimlib
print(manimlib.__file__)
def text_to_speech(text,file_name):
  v =gTTS(text=text,lang="en")
  v.save(file_name)

equation={
    4:-0.5,
    3:-5,
    2:5,
    1:8,
    0:1
}
boundary=(-1.5, 2)

def equation_to_polynomial(equation):
  max_degree=max(list(equation.keys()))
  polynomial_list=[]
  for deg in range(max_degree+1):
    try:
      polynomial_list.insert(0,equation[deg])
    except:
      polynomial_list.insert(0,0)
  return polynomial_list

def solve_polynomial(polynomial_dict):
  if type(polynomial_dict)==dict:
    polynomial_dict=equation_to_polynomial(polynomial_dict)
  all_roots=np.roots(polynomial_dict)
  real_roots=[round(solution.real,3) for solution in all_roots if solution.imag==0]
  return real_roots

def f_of_x(x):
  polynomial=0
  for power,coeff in equation.items():
    polynomial+=coeff*(x**power)
  return polynomial
def f_x(x,equation):
  max_degree=len(equation)-1
  solution=0
  for coeff,d in zip(equation,reversed(range(max_degree+1))):
    solution+=coeff*(x**d)
  return solution

def get_latex_of_integration(equation):
  max_degree=len(equation)
  equation_string=""
  for coeff,deg in zip(equation,reversed(range(max_degree-1))):
    if coeff >= 0:
      equation_string+=r"+"
      equation_string+=r"\frac{"+str(coeff)+r"}{"+str(deg+1)+r"}"+r"x^{"+str(deg+1)+r"}"
    else:
      equation_string+=r"\frac{"+str(coeff)+r"}{"+str(deg+1)+r"}"+r"x^{"+str(deg+1)+r"}"
  if equation[-1] >= 0:
    equation_string+=r"+"
  equation_string+=str(equation[-1])
  return equation_string

def get_latex_equation():
  degree = max(equation.keys())
  equation_string=""
  for deg in reversed(range(degree+1)):
    if equation[deg] >= 0:
      equation_string+=r"+"
    if deg==0:
      equation_string+=str(equation[deg])
    else:
      equation_string+=str(equation[deg])+r"x^{"+str(deg)+r"}"
  return equation_string

speech_collection={
    1:{"file_name":"intro.mp3","text":"welcome to V-math"},
    2:{
        "file_name":"draw_graph.mp3",
        "text":'''
        Let’s draw the graph of the given equation.
        '''},
    3:{
        "file_name":"between_points.mp3",
        "text":'''
        So, what I want to know, is the area under this curve,  between the points '''+str(boundary[0])+''' and '''+str(boundary[1])+'''.
        '''},
    4:{
        "file_name":"intercepts.mp3",
        "text":'''
        Before we do that, we need to check for any intersection points. 
        
        As you can see the polynomial crosses x axis in -0.29,0.56 and 1.39.
        '''},
    5:{
        "file_name":"required_area.mp3",
        "text":'''
        we are required to find the sum of these shaded areas 1,2,3 and 4
        '''},
}

for num in range(len(speech_collection)):
  text_to_speech(
      speech_collection[num+1]["text"],
      speech_collection[num+1]["file_name"]
  )

polynomial_solution=sorted(solve_polynomial(equation))
intercepts=sorted([root for root in polynomial_solution if boundary[0]<root<boundary[1]])

p_in_list=equation_to_polynomial(equation)
p_x = np.poly1d(p_in_list)
p_x1 = np.polyder(p_x)
p_x2 = np.polyder(p_x1)

inflection_points=[root for root in solve_polynomial(list(p_x1.coefficients)) if boundary[0]<root<boundary[1]]
inflection_values=[f_of_x(x) for x in inflection_points]
y_values_check=[f_of_x(boundary[0])] + inflection_values + [f_of_x(boundary[1])]

x_range=boundary[1]-boundary[0]
x_min=boundary[0]
x_max=boundary[1]
x_step=x_range/8
x_left=x_min-x_step
x_right=x_max+x_step
x_space=x_right-x_left

y_min=min(y_values_check)
y_max=max(y_values_check)
if y_min>0:
  y_min=-1
if y_max<0:
  y_max=1
y_range=y_max-y_min
y_step=y_range/8
y_left=y_min-y_step
y_right=y_max+y_step
y_space=y_right-y_left

space_unit_to_x = 9 / x_space
space_unit_to_y = 6 / y_space

x_labeled_nums = np.linspace(x_left,x_right,11)
y_labeled_nums = np.linspace(y_left,y_right,11)

class intro(Scene):
  def construct(self):
    self.add_sound("intro.mp3")
    math_v=TextMobject("V MATH").scale(2)
    self.play(ShowCreationThenDestruction(math_v),run_time=2)
    self.wait()

class draw_graph(GraphScene):
  CONFIG = {
    "camera_class": MovingCamera,
    "x_min": x_left,
    "x_max": x_right,
    "y_min": y_left,
    "y_max": y_right,
    "graph_origin":np.array([space_unit_to_x*(x_left+x_right)/-2,space_unit_to_y*(y_left+y_right)/-2,0]),
    "function_color": BLUE,
    "axes_color": RED,
    "x_labeled_nums":x_labeled_nums,
    "y_labeled_nums":y_labeled_nums,
    "x_tick_frequency":x_space/10,
    "y_tick_frequency":y_space/10,
    "Number_plane_config":{
         "number_scale_val": 0.5,
         "decimal_number_config": {
             "num_decimal_places": 2,
         },
    }
  }
  def construct(self):
    self.setup_axes(animate=True,**self.Number_plane_config)
    self.add_sound("draw_graph.mp3")

    func_graph=self.get_graph(f_of_x,self.function_color)
    graph_lable = self.get_graph_label(func_graph, label = get_latex_equation())
    self.play(ShowCreation(func_graph), Write(graph_lable),run_time=3)
    vert_line_left = self.get_vertical_line_to_graph(boundary[0],func_graph,color=YELLOW)
    vert_line_right = self.get_vertical_line_to_graph(boundary[1],func_graph,color=YELLOW)
    self.add_sound("between_points.mp3")
    self.wait(3)
    self.play(ShowCreation(vert_line_left),ShowCreation(vert_line_right))
    self.wait(2)
    intercept_dots=VGroup(*[Dot(self.coords_to_point(point,0)) for point in sorted(intercepts)])
    intercept_stamp=VGroup(*[TextMobject(str(point),color=GREEN).shift(self.coords_to_point(point,0)+0.5*UP).scale(0.5) for point in sorted(intercepts)])
    self.add_sound("intercepts.mp3")
    self.wait(5)
    self.play(FadeIn(intercept_dots))
    self.add_foreground_mobject(intercept_dots)
    self.play(FadeIn(intercept_stamp))
    self.wait(6)

    regions=sorted(intercepts)
    regions.insert(0,boundary[0])

    regions.append(boundary[-1])
    regions=[ x for x in zip(regions, regions[1:])]

    def get_coloured_graph(start,end):
      invert=0
      colour=BLUE_D
      area_sign=-1
      mid=start+end/2
      if (f_of_x(mid)>0):
        colour=GREEN
        area_sign=1
      graph=self.get_graph(
              f_of_x,
              x_min = start,
              x_max = end,
              color=YELLOW,
              opacity=0.5,
              fill_opacity=0.1,
              stroke_opacity=0.5
          )
      self.play(ShowCreationThenDestruction(graph),run_time=0.25)
      end_point_1 = graph.points[0]
      end_point_2 = graph.points[-1]
      axis_point = end_point_2[0]*RIGHT + self.graph_origin[1]*UP
      point = interpolate(axis_point, graph.points[-1], 0)
      graph.add_line_to(point)
      axis_point = end_point_1[0]*RIGHT + self.graph_origin[1]*UP
      point = interpolate(axis_point, graph.points[0], 0)
      graph.add_line_to(point)
      graph.set_stroke(width = 1)
      graph.set_fill(opacity = 1)
      graph.set_color(colour)
      return graph,area_sign

    graphs=[]
    area_sign=[]
    self.add_sound("required_area.mp3")
    graph=self.get_graph(
            f_of_x,
            x_min = self.x_min,
            x_max = self.x_max,
            color=YELLOW
        )
    region_count=1

    for region in regions:
      graph,sign=get_coloured_graph(region[0],region[1])
      region_lable=TextMobject(str(region_count)).scale(0.5).move_to(graph.get_center())
      self.play(FadeIn(graph),FadeIn(region_lable))
      graphs.append(graph)
      area_sign.append(sign)
      region_count+=1

    all_mobjects=Group(*self.mobjects)
    self.play(ApplyMethod(all_mobjects.scale,0.75))
    self.play(ApplyMethod(all_mobjects.shift,LEFT*4.5))
    self.wait()
    area_text=TextMobject("Area = ").scale(0.5).move_to(UR+2*UP+2*RIGHT)
    place_holder = area_text
    self.play(FadeIn(area_text))
    total_area=0
    p_integration=np.polyint(p_in_list)
    p_integration_text = get_latex_of_integration(p_in_list)
    area_place_holder=TexMobject(str(0)).scale(0.5).move_to(2*DR+3*UP)
#     new_total_area_text
    for region,sign,region_num in zip(regions,area_sign,range(len(regions))):
      area_solution=(f_x(region[-1],list(p_integration))-f_x(region[0],list(p_integration)))
      integral_sign=TexMobject("\int_{"+str(region[0])+"}^{"+str(region[1])+"}").scale(0.5).next_to(place_holder,2*DOWN)
      poly_text=TexMobject(get_latex_equation()).scale(0.5).next_to(integral_sign,RIGHT)
      self.play(FadeIn(integral_sign),FadeIn(poly_text))
      inte_text=TexMobject("="+p_integration_text).scale(0.5).next_to(poly_text,DOWN)
      self.play(FadeIn(inte_text))
      area_solution_text=TexMobject("="+str(round(area_solution*sign,2))).scale(0.5).next_to(inte_text,DOWN)
      total_area+=round(area_solution,2)*sign
      total_area_text=TexMobject(str(round(area_solution*sign,2))).scale(0.5).move_to(2*DR)
      self.play(FadeIn(area_solution_text))
      area_place_holder=total_area_text.deepcopy().next_to(area_place_holder,DOWN)
      self.play(FadeIn(area_place_holder))
      self.play(FadeOut(inte_text),FadeOut(integral_sign),FadeOut(poly_text),FadeOut(area_solution_text))
      
    final_area=TextMobject("Total area = "+str(round(total_area,2))).scale(0.8).next_to(area_place_holder,DOWN+0.5*RIGHT)
    self.play(FadeIn(final_area))
    self.wait(3)

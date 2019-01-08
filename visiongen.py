import sys

def create_hsv_filter(h, s, v):
    return "TargetFilter filter = new HSVFilter(new Range({}, {}), new Range({}, {}), new Range({}, {}));".format(h[0], h[1], s[0], s[1], v[0], v[1])

def create_fov(h_degrees, v_degrees):
    return "FOV fov = new FOV({}, {});".format(h_degrees, v_degrees)

def create_resolution(width, height):
    return "Resolution resolution = new Resolution({}, {});".format(width, height)

def create_inverted(inverted):
    return "boolean cameraInverted = {};".format(inverted)

def create_target_finder_variable():
    return "private TargetFinder targetFinder;"

def create_camera_settings():
    return "CameraSettings cameraSettings = new CameraSettings(cameraInverted, fov, resolution);"

def create_range(name, min_val, max_val):
    return "Range {} = new Range({}, {});".format(name, min_val, max_val)

def create_contour_filter():
    return "ContourFilter contourFilter = new StandardContourFilter(area, fullness, aspectRatio, imageArea);"

def create_target_finder():
    return "targetFinder = new TargetFinder(cameraSettings, filter, contourFilter, TargetGrouping.SINGLE);"

def create_image_area():
    return "int imageArea = resolution.getArea();"

def find_targets():
    return "return targetFinder.findTargets(image);"

def create_method():
    return "public List<Target> detectTargets(Mat image){"

def create_constructor(class_name):
    return "public " + class_name + "() {"

def create_class(class_name):
    return "public class " + class_name + " {"

def create_imports():
    return """import com.kylecorry.frc.vision.Range;
import com.kylecorry.frc.vision.camera.CameraSettings;
import com.kylecorry.frc.vision.camera.FOV;
import com.kylecorry.frc.vision.camera.Resolution;
import com.kylecorry.frc.vision.contourFilters.ContourFilter;
import com.kylecorry.frc.vision.contourFilters.StandardContourFilter;
import com.kylecorry.frc.vision.filters.HSVFilter;
import com.kylecorry.frc.vision.filters.TargetFilter;
import com.kylecorry.frc.vision.targetConverters.TargetGrouping;
import com.kylecorry.frc.vision.targeting.Target;
import com.kylecorry.frc.vision.targeting.TargetFinder;
import org.opencv.core.Mat;
import java.util.List;
    """

if len(sys.argv) != 2:
    print("Usage: python3 visiongen.py ClassName")
    exit(1)

class_name = sys.argv[1]

print("CAMERA PROPERTIES")
fov_h = input("Horizontal field of view (degrees): ")
fov_v = input("Vertical field of view (degrees): ")
res_width = input("Image width (pixels): ")
res_height = input("Image height (pixels): ")
camera_inverted = input("Camera inverted? [y/n]: ")
camera_inverted = "true" if camera_inverted == 'y' else "false"

print()
print("HSV FILTER PROPERTIES")
h_min = input("Min hue (0 - 180 degrees): ")
h_max = input("Max hue (0 - 180 degrees): ")
s_min = input("Min saturation (0 - 255): ")
s_max = input("Max saturation (0 - 255): ")
v_min = input("Min value (0 - 255): ")
v_max = input("Max value (0 - 255): ")

print()
print("CONTOUR PROPERTIES")
area_min = input("Min percent of image area: ")
area_max = input("Max percent of image area: ")
fullness_min = input("Min percent fullness: ")
fullness_max = input("Max percent fullness: ")
aspect_ratio_min = input("Min aspect ratio (width / height): ")
aspect_ratio_max = input("Max aspect ratio (width / height): ")

java_code = create_imports() + "\n"
java_code +=  "\n"
java_code += create_class(class_name) + "\n\n"
java_code += "\t" + create_target_finder_variable() + "\n\n"
java_code += "\t" + create_constructor(class_name) + "\n"
java_code += "\t\t" + create_range("area", area_min, area_max) + "\n"
java_code += "\t\t" + create_range("fullness", fullness_min, fullness_max) + "\n"
java_code += "\t\t" + create_range("aspectRatio", aspect_ratio_min, aspect_ratio_max) + "\n"
java_code +=  "\n"
java_code += "\t\t" + create_fov(fov_h, fov_v) + "\n"
java_code += "\t\t" + create_resolution(res_width, res_height) + "\n"
java_code += "\t\t" + create_inverted(camera_inverted) + "\n"
java_code += "\t\t" + create_image_area() + "\n"
java_code +=  "\n"
java_code += "\t\t" + create_camera_settings() + "\n"
java_code += "\t\t" + create_hsv_filter((h_min, h_max), (s_min, s_max), (v_min, v_max)) + "\n"
java_code += "\t\t" + create_contour_filter() + "\n"
java_code += "\t\t" + create_target_finder() + "\n"
java_code += "\t}" + "\n"

java_code +=  "\n"
java_code += "\t" + create_method() + "\n"
java_code += "\t\t" + find_targets() + "\n"
java_code += "\t}" + "\n"
java_code += "}" + "\n\n"

with open(class_name + ".java", 'w') as f:
    f.write(java_code)

print(java_code)

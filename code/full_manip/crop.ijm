args = split(getArgument(), ",");
file = args[0];
x = parseInt(args[1]);
y = parseInt(args[2]);
w = parseInt(args[3]);
h = parseInt(args[4]);

inputPath = file;
outputDir = "./out/";

run("TIFF Virtual Stack...", "open=[" + inputPath + "]");

makeRectangle(x, y, w, h);
run("Crop");

saveAs("Tiff", outputDir + "out.tif");

close();

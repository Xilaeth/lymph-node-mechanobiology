inputPath = "788-P7175_Actin_LA(Piringer)_thresholded.ome.tif";
outputDir = "./out/";

run("TIFF Virtual Stack...", "open=[" + inputPath + "]");

x = 4800; y = 5800; width = 1000; height = 1000;

makeRectangle(x, y, width, height);
run("Crop");

saveAs("Tiff", outputDir + "out.tif");
close();

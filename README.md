# OCTCode
image processing pipeline for OCT image scans, uses openCV libraries

General pipeline structures:

-2x recursive median blurring (tried gaussian and bilateral but they only introduced more irregularities)

-manual black/white threshold (tried OTSU thresholding but it curves gradient shapes, other papers have tried developing their own automatic thresholder)

-sobely edge detection, kernel size 3, single derivation in the y direction

-probabalistic hugh line dectection (alter parameters as needed for cleaner lines)

# OCTDepthPipeline
-detects y displacement between lines

# OCTWidthPipeline
-detects x distance between edges of lines

# BoundaryTest
-detects more organic shapes to varying degrees of succes, depends largely on prefiltering and thresholding
-OTSU auto thresholding exists but I have had much success with it

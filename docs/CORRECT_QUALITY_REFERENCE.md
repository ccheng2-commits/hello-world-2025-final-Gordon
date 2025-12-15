# Correct Quality Reference Images

## ✅ Verified Correct Images: 4, 5, 6, 8, 9, 10, 11

These 7 images have been verified as correct processing results and serve as the quality reference.

### Quality Characteristics

| Image | Size | Resolution | Orig Brightness | Orig Contrast | Proc Non-zero | Center | Edge |
|-------|------|------------|-----------------|---------------|---------------|--------|------|
| incoming-004 | 299x168 | 50,232 | 153.7 | 66.4 | 43.2% | 29.7 | 66.9 |
| incoming-005 | 275x183 | 50,325 | 162.1 | 62.7 | 44.3% | 49.1 | 71.0 |
| incoming-006 | 275x183 | 50,325 | 161.7 | 62.7 | 44.3% | 48.8 | 70.7 |
| incoming-008 | 612x612 | 374,544 | 24.6 | 47.4 | 8.8% | 8.8 | 0.0 |
| incoming-009 | 390x280 | 109,200 | 142.2 | 66.1 | 43.1% | 49.9 | 51.2 |
| incoming-010 | 910x511 | 465,010 | 142.9 | 65.6 | 48.2% | 30.9 | 93.8 |
| incoming-011 | 500x667 | 333,500 | 166.9 | 63.7 | 50.1% | 29.3 | 102.9 |

### Quality Ranges

- **Resolution**: 50,232 - 465,010 pixels
- **Original Brightness**: 24.6 - 166.9
- **Original Contrast**: 47.4 - 66.4
- **Processed Non-zero**: 8.8% - 50.1%
- **Processed Center**: 8.8 - 49.9
- **Processed Edge**: 51.2 - 102.9

### Key Observations

1. **Resolution Range**: Wide range acceptable (50K to 465K pixels)
2. **Brightness Range**: Very wide (24.6 to 166.9) - includes very dark images (008)
3. **Contrast**: Consistent range (47.4 - 66.4)
4. **Processed Content**: Varies significantly (8.8% to 50.1%)
   - Note: Image 008 has only 8.8% non-zero but is still correct
5. **Donut Structure**: Most have clear center/edge contrast, but 008 is very dark overall

### Notes

- **Image 008** is very dark (brightness 24.6) and uses fallback method, but result is correct
- **Images 4, 5, 6, 9, 10, 11** successfully detected pupils
- These images represent the acceptable quality standard for the project

### Usage

Use these images as reference when:
- Evaluating processing quality
- Setting quality thresholds
- Testing algorithm improvements
- Comparing new processing results







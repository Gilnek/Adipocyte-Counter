import typer
from cv2 import imwrite
from pathlib import Path

from adpcount import adp_count
from adpcount_watershed import adp_count_watershed

app = typer.Typer()

@app.command()
def count(image: str, out: str = "out.png",
        img_gray: str = "gray.png",
        img_thresh: str = "threshold.png",
        img_mask: str = "mask.png") -> None:
    count, out_mat = adp_count(image_path=image,
        return_image=True,
        img_gray=img_gray,
        img_thresh=img_thresh,
        img_mask=img_mask)
    print(f"Adipocitos encontrados: {count}")
    imwrite(out, out_mat)

@app.command()
def watershed(image: str, out: str = "out.png",
        img_gray: str = "gray.png",
        img_thresh: str = "threshold.png",
        img_mask: str = "mask.png") -> None:
    count, out_mat = adp_count_watershed(image_path=image,
        return_image=True,
        img_gray=img_gray,
        img_thresh=img_thresh,
        img_mask=img_mask)
    print(f"Adipocitos encontrados: {count}")
    imwrite(out, out_mat)

if __name__ == '__main__':
    app()

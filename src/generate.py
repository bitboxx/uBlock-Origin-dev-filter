from glob import glob
from pathlib import Path

LINE_SEP = "\n"

def to_css_attr(url):
    return url.replace("*://", "").replace("*.", ".").replace("/*", "")

def to_google(url):
    return f'google.*##.g:has(a[href*="{to_css_attr(url)}"])'

def to_duckduckgo(url):
    return f'duckduckgo.*##.results > div:has(a[href*="{to_css_attr(url)}"])'

def to_brave(url):
    return f'search.brave.com###results > div:has(a[href*="{to_css_attr(url)}"])'

def to_startpage(url):
    return f'startpage.com##.w-gl__result:has(a[href*="{to_css_attr(url)}"])'

def main():
    root_path = Path(__file__).parent.joinpath("../")
    dist_path = root_path.joinpath("dist")

    g_all = dist_path.joinpath("google", "all.txt")
    d_all = dist_path.joinpath("duckduckgo", "all.txt")
    gd_all = dist_path.joinpath("google_duckduckgo", "all.txt")
    b_all = dist_path.joinpath("brave", "all.txt")
    sp_all = dist_path.joinpath("startpage", "all.txt")

    for f in [g_all, d_all, gd_all, b_all, sp_all]:
        f.parent.mkdir(parents=True, exist_ok=True)

    with g_all.open("w") as g_all, \
         d_all.open("w") as d_all, \
         gd_all.open("w") as gd_all, \
         b_all.open("w") as b_all, \
         sp_all.open("w") as sp_all:

        for file in root_path.joinpath("data").glob("*.txt"):
            filename = file.name.split(".")[0]

            with dist_path.joinpath("google", f"{filename}.txt").open("w") as g, \
                dist_path.joinpath("duckduckgo", f"{filename}.txt").open("w") as d, \
                dist_path.joinpath("google_duckduckgo", f"{filename}.txt").open("w") as gd, \
                dist_path.joinpath("brave", f"{filename}.txt").open("w") as b, \
                dist_path.joinpath("startpage", f"{filename}.txt").open("w") as sp, \
                file.open("r") as i:
                for line in i:
                    if line.startswith("!") or not line.strip():
                        continue
                    url = line.strip()
                    for f in [
                        g, g_all,
                        d, d_all,
                        gd, gd_all,
                        b, b_all,
                        sp, sp_all
                    ]:
                        f.write(url + LINE_SEP)

                    url_google = to_google(url)
                    url_duckduckgo = to_duckduckgo(url)
                    url_brave = to_brave(url)
                    url_sp = to_startpage(url)
                    for f in [
                        g, g_all,
                        gd, gd_all
                    ]:
                        f.write(url_google + LINE_SEP)
                    for f in [
                        d, d_all,
                        gd, gd_all
                    ]:
                        f.write(url_duckduckgo + LINE_SEP)
                    for f in [
                        b, b_all
                    ]:
                        f.write(url_brave + LINE_SEP)
                    for f in [
                        sp, sp_all
                    ]:
                        f.write(url_sp + LINE_SEP)

if __name__ == "__main__":
    main()
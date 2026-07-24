"""
Decode is memory-bandwidth bound: the back-of-envelope token-cost calculator.

Companion code for:
  https://vexpose.blog/  (The Inference Bill Is a Memory-Bandwidth Problem)

For a memory-bound decode, each generated token requires reading the whole model's
weights out of HBM once. So the single-stream ceiling is set by bandwidth, not FLOPs:

    bytes_per_token   = params * bytes_per_param
    time_per_token    = bytes_per_token / hbm_bandwidth
    tokens_per_second = 1 / time_per_token

These are ceilings from bandwidth alone; real systems land below them (kernel,
compute, networking overhead). But the RANKING holds, and it tells you the tell:
the intervention that helps is the one that moves FEWER bytes (quantization), not
the one that adds more math (a bigger GPU).
"""

from dataclasses import dataclass


@dataclass
class Model:
    name: str
    params_b: float          # billions of parameters
    bytes_per_param: float   # 2.0 = FP16, 1.0 = FP8, 0.5 = INT4


def estimate(model: Model, hbm_tb_s: float = 2.0) -> dict:
    bytes_per_token = model.params_b * 1e9 * model.bytes_per_param
    hbm_bytes_s = hbm_tb_s * 1e12
    time_per_token = bytes_per_token / hbm_bytes_s
    return {
        "model": model.name,
        "gb_per_token": round(bytes_per_token / 1e9, 1),
        "hbm_tb_s": hbm_tb_s,
        "ms_per_token": round(time_per_token * 1e3, 1),
        "tok_per_s": round(1 / time_per_token, 0),
    }


if __name__ == "__main__":
    HBM = 2.0  # TB/s — representative of an 80GB-class accelerator; change for yours
    fleet = [
        Model("7B  FP16", 7, 2.0),
        Model("13B FP16", 13, 2.0),
        Model("70B FP16", 70, 2.0),
        Model("70B FP8", 70, 1.0),
    ]
    rows = [estimate(m, HBM) for m in fleet]
    w = max(len(r["model"]) for r in rows)
    print(f"{'model':<{w}}  {'GB/token':>9}  {'TB/s':>5}  {'ms/token':>9}  {'tok/s':>7}")
    for r in rows:
        print(f"{r['model']:<{w}}  {r['gb_per_token']:>9}  {r['hbm_tb_s']:>5}  "
              f"{r['ms_per_token']:>9}  {int(r['tok_per_s']):>7}")
    print("\nFP16 -> FP8 halves bytes/token and ~doubles decode throughput: "
          "you cut the bottleneck, you didn't add compute.")

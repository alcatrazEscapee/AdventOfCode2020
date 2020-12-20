# Day 20: Jurassic Jigsaw
# Results: 1726 / 243

from utils import *


def main():
    sample1, sample2 = run(get_input('./example_input.txt'))

    assert sample1 == 20899048083289
    assert sample2 == 273

    part1, part2 = run(get_input())
    print('Part 1:', part1)
    print('Part 2:', part2)


def run(text: str, do_visualizations: bool = False) -> Tuple[int, int]:
    # Parse tiles into Grids
    tiles = {}
    for group in text.split('\n\n'):
        key, *lines = group.strip().split('\n')
        key = ints(key)[0]
        g = Grid.from_lines(lines)
        tiles[key] = g

    # Sanity checks and dimension calculations
    g = next(v for v in tiles.values())
    assert g.width == g.height

    size = g.width
    interior = size - 2
    square = isqrt(len(tiles))

    # Build the entire puzzle (computes part 1 and prepares part 2)
    assembled = build_puzzle(tiles, size, square)
    corner_indices = (0, square - 1, (square - 1) * square, square * square - 1)
    corner_checksum = prod(assembled[i][0] for i in corner_indices)

    # Assemble the joined grid (without edge overlaps)
    cols = []
    for y in range(square * interior):
        row = []
        ty = y // interior
        ly = y % interior + 1
        for x in range(square * interior):
            tx = x // interior
            lx = x % interior + 1
            row.append(assembled[tx + square * ty][1][lx, ly])
        cols.append(row)
    joined = Grid(cols, default_value='X')  # Default value is set to X - this way we can check easily outside this area for sea monsters and it will immediately abort

    if do_visualizations:
        print(joined)

    sea_monster = Grid.from_text(SEA_MONSTER)

    # Iterate through each variant of the joined grid (rotations and mirrors)
    # Only one will report any sea monsters
    for joined_variant in joined.permutations():
        sea_monster_positions = set()

        # x, y is the origin position for a potential sea monster
        # dx, dy is the offset of that pos to the sea monster grid
        # If the sea monster is '#' (at dx, dy), then the real grid must be either '#' or '.' ('X' means out of bounds and will abort)
        for x, y in joined_variant.locations():
            temp_monster_pos = set()
            for dx, dy in sea_monster.locations():
                x0 = x + dx
                y0 = y + dy
                if sea_monster[dx, dy] == '#':
                    if joined_variant[x0, y0] != '#':
                        break
                    temp_monster_pos.add((x0, y0))
            else:
                for p in temp_monster_pos:
                    sea_monster_positions.add(p)

        if len(sea_monster_positions) > 0:
            # Found sea monsters!
            return corner_checksum, joined_variant.count('#') - len(sea_monster_positions)
    raise RuntimeError('No sea monsters found in any variant')


def build_puzzle(tiles: Dict[int, Grid], size: int, square: int) -> List[Tuple[int, Grid]]:
    """
    Builds a puzzle from an initial mapping of tile IDs -> Grids
    This records each tile ID, and the actual tile (including rotations or mirrors), as both are used in part 1 and part 2 respectively
    The basic algorithm is a BFS, which checks each new location against every possible new piece, and if the piece fits, considers that a new node
    """
    queue: List[Tuple[List[Optional[Tuple[int, Grid]]], int, Set[int]]] = [([None] * square * square, 0, set())]
    tile_variants: Dict[int, List[Grid]] = dict((tile_id, list(tile.permutations())) for tile_id, tile in tiles.items())
    while queue:
        puzzle, next_idx, used = queue.pop()
        for tile_id, tile in tiles.items():
            if tile_id not in used:
                next_x = next_idx % square
                next_y = (next_idx // square) % square
                for variant in tile_variants[tile_id]:
                    if connects(puzzle, next_x, next_y, variant, size, square):
                        new_puzzle = list(puzzle)
                        new_puzzle[next_idx] = (tile_id, variant)
                        new_used = set(used)
                        new_used.add(tile_id)
                        if next_idx == len(new_puzzle) - 1:
                            return new_puzzle
                        else:
                            queue.append((new_puzzle, next_idx + 1, new_used))
    raise RuntimeError('No solution to the puzzle')


def connects(puzzle: List[Optional[Tuple[int, Grid]]], xt: int, yt: int, tile: Grid, size: int, square: int):
    """
    This tests that the new piece matches existing pieces
    Due to the order in which we assemble the pieces, we only need to test the UP and LEFT locations
    """
    if xt - 1 >= 0:
        left = puzzle[(xt - 1) + yt * square]
        if left is not None:
            left = left[1]
            for y in range(tile.height):
                if left[size - 1, y] != tile[0, y]:
                    return False
    if yt - 1 >= 0:
        top = puzzle[xt + (yt - 1) * square]
        if top is not None:
            top = top[1]
            for x in range(size):
                if top[x, size - 1] != tile[x, 0]:
                    return False
    return True


SEA_MONSTER = """
..................#.
#....##....##....###
.#..#..#..#..#..#...
"""


if __name__ == '__main__':
    main()

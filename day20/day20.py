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
    # Parse tiles into grids
    tiles = {}
    for group in text.split('\n\n'):
        key, *lines = group.strip().split('\n')
        tiles[ints(key)[0]] = Grid.from_lines(lines)

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

    if do_visualizations:
        exterior = size + 1

        def joined_bordered_lambda(x_: int, y_: int) -> str:
            px, py = x_ % exterior, y_ % exterior
            if px < size and py < size:
                return assembled[(x_ // exterior) + square * (y_ // exterior)][1][px, py]
            return ' '

        joined_bordered = Grid.from_function(square * exterior, square * interior, joined_bordered_lambda, default_value='X')
        print('Assembled Pieces:\n%s\n' % joined_bordered)

        def joined_ids_lambda(x_: int, y_: int) -> str:
            return str(assembled[(x_ // 2) + square * (y_ // 2)][0]) if x_ % 2 == 0 and y_ % 2 == 0 else ' '

        joined_ids = Grid.from_function(square * 2, square * 2, joined_ids_lambda)
        print('Assembled Piece IDs:\n%s\n' % joined_ids)

    # Assemble the joined grid (without edge overlaps)
    # Default value is set to X - this way we can check easily outside this area for sea monsters and it will immediately abort
    def joined_lambda(x_: int, y_: int) -> str:
        return assembled[(x_ // interior) + square * (y_ // interior)][1][x_ % interior + 1, y_ % interior + 1]
    joined = Grid.from_function(square * interior, square * interior, joined_lambda, default_value='X')
    sea_monster = Grid.from_text(SEA_MONSTER)

    if do_visualizations:
        print('Joined:\n%s\n' % joined)
        print('Sea Monster:\n%s\n' % sea_monster)

    # Iterate through each variant of the joined grid (rotations and mirrors)
    # Only one will report any sea monsters
    for joined_variant in joined.permutations():
        sea_monster_positions = set()

        # x, y is the origin position for a potential sea monster
        # dx, dy is the offset of that pos to the sea monster grid
        # If the sea monster is '#' (at dx, dy), then the real grid must be '#' (at pos)
        for x, y in joined_variant.locations():
            temp_monster_pos = set()
            for dx, dy in sea_monster.locations():
                pos = x + dx, y + dy
                if sea_monster[dx, dy] == '#':
                    if joined_variant[pos] != '#':
                        break
                    temp_monster_pos.add(pos)
            else:
                for p in temp_monster_pos:
                    sea_monster_positions.add(p)

        if len(sea_monster_positions) > 0:  # Found sea monsters!

            if do_visualizations:
                joined_with_sea_monsters = joined_variant.copy()
                for x, y in sea_monster_positions:
                    joined_with_sea_monsters[x, y] = 'O'
                print('Located Sea Monsters:\n%s\n' % joined_with_sea_monsters)

            return corner_checksum, joined_variant.count('#') - len(sea_monster_positions)
    raise RuntimeError('No sea monsters found in any variant')


def build_puzzle(tiles: Dict[int, Grid], size: int, square: int) -> List[Tuple[int, Grid]]:
    """
    Builds a puzzle from an initial mapping of tile IDs -> Grids
    This records each tile ID, and the actual tile (including rotations or mirrors), as both are used in part 1 and part 2 respectively
    The basic algorithm is a DFS (which in this case, due to may valid assemblies (one per 8 permutations) is about 6x faster overall than the BFS, which checks each new location against every possible new piece, and if the piece fits, considers that a new node
    The puzzle is a list of all pieces, indexed via x + y * size
    """
    stack: List[Tuple[List[Tuple[int, Grid]], int, Set[int]]] = [([], 0, set())]
    tile_variants: Dict[int, Tuple[Grid]] = dict((tile_id, tuple(tile.permutations())) for tile_id, tile in tiles.items())
    while stack:
        puzzle, next_idx, used = stack.pop(-1)
        for tile_id, tile in tiles.items():
            if tile_id not in used:
                next_x = next_idx % square
                next_y = (next_idx // square) % square
                for variant in tile_variants[tile_id]:
                    if connects(puzzle, next_x, next_y, variant, size, square):
                        new_puzzle = list(puzzle)
                        new_puzzle.append((tile_id, variant))
                        new_used = set(used)
                        new_used.add(tile_id)
                        if next_idx == square * square - 1:
                            return new_puzzle
                        else:
                            stack.append((new_puzzle, next_idx + 1, new_used))
    raise RuntimeError('No solution to the puzzle')


def connects(puzzle: List[Tuple[int, Grid]], xt: int, yt: int, tile: Grid, size: int, square: int):
    """
    This tests that the new piece matches existing pieces
    Due to the order in which we assemble the pieces, we only need to test the UP and LEFT locations
    We can also skip on puzzle bounds checks (except for the negative indices) as the adjacent pieces will never be empty, only out of bounds.
    """
    if xt - 1 >= 0:
        left = puzzle[(xt - 1) + yt * square][1]
        if any(left[size - 1, y] != tile[0, y] for y in range(size)):
            return False

    if yt - 1 >= 0:
        top = puzzle[xt + (yt - 1) * square][1]
        if any(top[x, size - 1] != tile[x, 0] for x in range(size)):
            return False
    return True


SEA_MONSTER = """
..................#.
#....##....##....###
.#..#..#..#..#..#...
"""


if __name__ == '__main__':
    main()

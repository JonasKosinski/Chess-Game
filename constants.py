import numpy as np

Tile_Size = 70  # Size of chess tiles
Tile_Color = (100, 30, 30)  # Color of chess tiles
Border_Width = Tile_Size // 2
Origin = (Border_Width, Border_Width)  # Origin point of the chess board
Window_Size = (Tile_Size * 8) + (Border_Width * 2)
button_width = (Tile_Size * 3) // 4
slot_width = Tile_Size * 2 + (Tile_Size // 10)
slot_length = Tile_Size * 4

# Creates arrays of bitboards where each bit board has a file/rank filled with ones
ranks = np.flip(np.array([np.uint64(0x00000000000000FF) << np.uint8(8 * i) for i in range(8)], dtype=np.uint64))
files = np.flip(np.array([np.uint64(0x0101010101010101) << np.uint8(i) for i in range(8)], dtype=np.uint64))

# Bitboards with the diagonal and anti-diagonal lines filled
anti_diagonal = np.uint64(0x8040201008040201)
diagonal = np.uint64(0x0102040810204080)

# Bitboard with first bit being one and the rest being zero
bb_first = np.uint64(9223372036854775808)

bb_tiles = np.array([bb_first >> np.uint8(i) for i in range(64)])

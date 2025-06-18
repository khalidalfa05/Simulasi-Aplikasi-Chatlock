def create_matrix(key):
    key = key.upper().replace("J", "I")
    seen = set()
    matrix = []

    for char in key:
        if char.isalpha() and char not in seen:
            seen.add(char)
            matrix.append(char)

    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in seen:
            seen.add(char)
            matrix.append(char)

    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None

def process_text(text):
    text = text.upper().replace("J", "I")
    filtered = [c for c in text if c.isalpha()]
    result = ""
    i = 0
    while i < len(filtered):
        a = filtered[i]
        b = filtered[i+1] if i+1 < len(filtered) else "X"
        if a == b:
            result += a + "X"
            i += 1
        else:
            result += a + b
            i += 2
    if len(result) % 2 != 0:
        result += "X"
    return result

def encrypt(text, key):
    matrix = create_matrix(key)
    space_positions = [i for i, c in enumerate(text) if c == ' ']

    clean_text = text.upper()
    filtered = ''.join(c for c in clean_text if c.isalpha())
    processed = process_text(filtered)
    ciphertext = ""

    for i in range(0, len(processed), 2):
        a, b = processed[i], processed[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            ciphertext += matrix[row1][(col1 + 1) % 5]
            ciphertext += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += matrix[(row1 + 1) % 5][col1]
            ciphertext += matrix[(row2 + 1) % 5][col2]
        else:
            ciphertext += matrix[row1][col2]
            ciphertext += matrix[row2][col1]

    for pos in space_positions:
        ciphertext = ciphertext[:pos] + ' ' + ciphertext[pos:]

    return ciphertext, processed  # ⬅️ return tambahan: processed

def decrypt(text, key):
    matrix = create_matrix(key)
    space_positions = [i for i, c in enumerate(text) if c == ' ']

    filtered = ''.join(c for c in text if c.isalpha())
    plaintext = ""

    for i in range(0, len(filtered), 2):
        a, b = filtered[i], filtered[i+1]

        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            plaintext += matrix[row1][(col1 - 1) % 5]
            plaintext += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]
        else:
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]

    for pos in space_positions:
        plaintext = plaintext[:pos] + ' ' + plaintext[pos:]

    return plaintext

from ctypes import CDLL, create_string_buffer, POINTER, c_ulonglong, byref, string_at

luau_dll = CDLL("./luau.dll")

luau_compile = luau_dll.luau_compile
luau_compress = luau_dll.luau_compress
luau_decompress = luau_dll.luau_decompress

def create_buffer(source: bytes) -> tuple:
    return (
        create_string_buffer(source),
        POINTER(c_ulonglong)(),
        c_ulonglong()
    )

class Luau:
    def compile(source: str, optimizationLevel: int = 2, debugLevel: int = 2) -> bytes:
        source_bytes: bytes = source.encode("utf-8", "ignore")
        source_buffer, output, out_size = create_buffer(source_bytes)
        luau_compile(
            source_buffer, len(source_bytes),
            byref(output), byref(out_size),
            optimizationLevel, debugLevel
        )

        return string_at(output, out_size.value)
    
    def compress(bytecode: bytes) -> bytes:
        bytecode_buffer, output, out_size = create_buffer(bytecode)
        luau_compress(
            bytecode_buffer, len(bytecode),
            byref(output), byref(out_size)
        )

        return string_at(output, out_size.value)
    
    def decompress(bytecode: bytes) -> bytes:
        bytecode_buffer, output, out_size = create_buffer(bytecode)

        luau_decompress(
            bytecode_buffer, len(bytecode),
            byref(output), byref(out_size)
        )

        return string_at(output, out_size.value)
import ctypes

dll = ctypes.CDLL("./bin/luau.dll")

luauCompile = dll.luau_compile
luauCompress = dll.luau_compress
luauDecompress = dll.luau_decompress

def createBuffer(source: bytes) -> tuple:
    return (
        ctypes.create_string_buffer(source),
        ctypes.POINTER(ctypes.c_ulonglong)(),
        ctypes.c_ulonglong()
    )

class Luau:
    def compile(source: str, optimizationLevel: int = 2, debugLevel: int = 2) -> bytes:
        sourceBytes: bytes = source.encode("utf-8", "ignore")
        sourceBuffer, output, outSize = createBuffer(sourceBytes)
        luauCompile(
            sourceBuffer, len(sourceBytes),
            ctypes.byref(output), ctypes.byref(outSize),
            optimizationLevel, debugLevel
        )

        return ctypes.string_at(output, outSize.value)
    
    def compress(bytecode: bytes) -> bytes:
        bytecodeBuffer, output, outSize = createBuffer(bytecode)
        luauCompress(
            bytecodeBuffer, len(bytecode),
            ctypes.byref(output), ctypes.byref(outSize)
        )

        return ctypes.string_at(output, outSize.value)
    
    def decompress(bytecode: bytes) -> bytes:
        bytecodeBuffer, output, outSize = createBuffer(bytecode)
        luauDecompress(
            bytecodeBuffer, len(bytecode),
            ctypes.byref(output), ctypes.byref(outSize)
        )

        return ctypes.string_at(output, outSize.value)
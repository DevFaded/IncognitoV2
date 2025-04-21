# Basic Offsets

RENDERJOB_RENDERVIEW = 0x1E8
DATAMODEL_HOLDER     = 0x118
REAL_DATAMODEL       = 0x1A8

INST_SELF            = 0x8
INST_CDESCRIPTOR     = 0x18
INST_PARENT          = 0x50
INST_NAME            = 0x68
INST_CHILDREN        = 0x70
VALUEBASE_VALUE      = 0xC8

MDESC_NAME           = 0x8
MDESC_SECURITY       = 0x38

CDESC_PROPERTIES     = 0x28     # PropertyDescriptors
CDESC_METHODS        = 0x178    # BoundFuncDescriptors
CDESC_CAPABILITIES   = 0x370    # Class Capabilities

# Script Offsets

LSCPT_EMBEDDEDCODE   = 0x1C0    # LocalScript EmbeddedCode Offset
MSCPT_EMBEDDEDCODE   = 0x168    # ModuleScript EmbeddedCode Offset
BSCPT_WTHRDREFNODE   = 0x198    # BaseScript's Node (contains luastate) only for LocalScripts and CoreScripts, ModuleScripts uses PerVMState

EMBDC_BYTECODE       = 0x10     # EmbeddedCode -> Bytecode
EMBDC_BYTECODESIZE   = 0x20     # Bytecode's Size

MSCPT_VMSTATEMAP     = 0x1C0    # ModuleScript's StateMap
VMSTM_LOADINGSTATE   = 0x20     # VmState's Loading State
VMSTM_WTHRDREFNODE   = 0x28     # VmState's Node (Contains lua state)
VMSTM_GLOBALSTATE    = 0x30     # VmState's GlobalState

# Script Context & Lua State Offsets

SCNTXT_GLOBALSTATE   = 0x248    # ScriptContext's GlobalState
SCNTXT_MAXCAPS       = 0x6A0    # Max capabilities for scripts
SCNTXT_ALWNRBXSCPTS  = 0x6E0    # Allow non RobloxScripts for require

LSTATE_EXTRASPACE    = 0x78     # LuaState -> ExtraSpace

ESPACE_NEXT          = 0x10
ESPACE_SHARED        = 0x18
ESPACE_WTHRDREFNODE  = 0x28
ESPACE_IDENTITY      = 0x30
ESPACE_CAPABILITIES  = 0x48
ESPACE_SCRIPT        = 0x50

WTHRDREF_PREVIOUS    = 0x10
WTHRDREF_NEXT        = 0x18
WTHRDREF_LTHRDREF    = 0x20
WTHRDREF_NODE        = 0x28

WTHRDREFNODE_FIRST   = 0x8      # WeakThreadRefNode -> WeakThreadRef
LTHRDREF_THREAD      = 0x8      # LiveThreadRef/WeakThreadRef -> LuaState

CAPABILITIES_ENC     = 0x3FFFFFF00

# Bindable & FunctionScriptSlotImpl Offsets

BNDABLEVT_EVTS       = 0xC0     # BindableEvent's Events
EVNTCONN_COUNT       = 0x4      # Event Connection Count
EVNTCONN_FIRST       = 0x8      # Event First Connection

CONN_NEXT            = 0x10     # Connection -> Next
CONN_PREVIOUS        = 0x18     # Connection -> Previous
CONN_FUNCSCPTSLOT    = 0x30     # Connection -> FunctionScriptSlotImpl

FUNCSCPTSLOT_ROOT    = 0x8      # FunctionScriptSlotImpl's Root
FUNCSCPTSLOT_NAME    = 0x28     # FunctionScriptSlotImpl's Name
FUNCSCPTSLOT_THRDREF = 0x60     # Sometimes its WeakObjectRef
FUNCSCPTSLOT_FUNC    = 0x70     # FunctionScriptSlotImpl's Function

# Distance between gcjob and allownonrbxscripts are 0x188 (can be used to get allownonrbxscripts offset easily)
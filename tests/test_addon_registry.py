from musicstudio.addons.manifest import AddonManifest, AddonRegistry, AddonType


def test_addon_registry_registers_and_finds():
    registry = AddonRegistry()
    addon = AddonManifest(
        id="demo.analyzer",
        name="Demo Analyzer",
        version="0.1.0",
        type=AddonType.analyzer,
        capabilities=["bpm"],
    )
    registry.register(addon)

    assert registry.get("demo.analyzer") == addon
    assert registry.by_type(AddonType.analyzer) == [addon]

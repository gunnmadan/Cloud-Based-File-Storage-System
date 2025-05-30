from app import create_app

app = create_app()

with app.app_context():
    print("==== Registered Flask Routes ====")
    for rule in app.url_map.iter_rules():
        print(f"{list(rule.methods)} -> {rule.rule}")

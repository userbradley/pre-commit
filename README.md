# Pre-commit hooks

<!-- TOC -->
* [Pre-commit hooks](#pre-commit-hooks)
  * [Using](#using)
  * [Snippets](#snippets)
    * [Core Rules](#core-rules)
    * [Correct Examples](#correct-examples)
    * [Incorrect examples](#incorrect-examples)
<!-- TOC -->

## Using

```yaml
repos:
  - repo: https://github.com/userbradley/pre-commit
    rev: v0.0.4
    hooks:
      - id: check-snippets
```

## Snippets

### Core Rules

1.  **Matching Pairs**: Every `# [START ...]` tag must have a corresponding `# [END ...]` tag.
2.  **Identical Naming**: The name inside a `START` tag must exactly match the name in its corresponding `END` tag. Naming is case-sensitive.
3.  **No Nesting**: You cannot start a new snippet before the previous one has been closed. Snippets must be sequential.

### Correct Examples

A single, valid snippet:

```python
# [START create_user]
def create_user(username, password):
  # function implementation...
  return User(username)
# [END create_user]
```

Multiple snippets in the same file

```python
# [START initialize_database]
db = connect_to_database()
# [END initialize_database]

# [START fetch_products]
products = db.query("SELECT * FROM products;")
# [END fetch_products]
```

### Incorrect examples

Not matching

```shell
# [START send_message]
def send_message(recipient, body):
  # ...
# [END send_email]  # <--- INVALID: Name does not match 'send_message'.
```

Nested

```python
# [START get_user_profile]
user = get_user(id=123)
# [START get_address]      # <--- INVALID: Cannot start a new snippet here.
address = user.address
# [END get_user_profile]
```

Unclosed

```python
# [START log_event]
def log_event(message):
  print(f"[{datetime.now()}]: {message}")
# File ends here <--- INVALID: Missing '[END log_event]'.
```

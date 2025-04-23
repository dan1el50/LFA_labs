def print_ast(node, indent="", is_last=True):
    marker = "└── " if is_last else "├── "

    if hasattr(node, 'value') and not hasattr(node, 'left'):
        # NumberNode
        print(indent + marker + f"Number({node.value})")
    elif hasattr(node, 'operand'):
        # UnaryOpNode
        print(indent + marker + f"Function({node.operator})")
        print_ast(node.operand, indent + ("    " if is_last else "│   "), True)
    elif hasattr(node, 'left') and hasattr(node, 'right'):
        # BinaryOpNode
        print(indent + marker + f"Operation({node.operator})")
        print_ast(node.left, indent + ("    " if is_last else "│   "), False)
        print_ast(node.right, indent + ("    " if is_last else "│   "), True)
    else:
        # Fallback for unexpected nodes
        print(indent + marker + "UnknownNode")

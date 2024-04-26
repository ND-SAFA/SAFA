def extract_alternate_names(string_list):
    result = []

    # Iterate over each string in the list
    for string in string_list:
        main_name = []
        alternate_names = []
        is_in_parenthesis = False
        current_name = []

        # Iterate over each character in the string
        for char in string:
            if char == "(":
                # When encountering '(', complete the main name
                if not is_in_parenthesis:
                    is_in_parenthesis = True
                    if current_name:
                        # Join the main name and clear the buffer
                        main_name.append("".join(current_name).strip())
                        current_name = []
            elif char == ")":
                # When encountering ')', complete the alternate name
                if is_in_parenthesis:
                    alternate_names.append("".join(current_name).strip())
                    current_name = []
                    is_in_parenthesis = False
            else:
                # Collect characters for the current name
                current_name.append(char)

        # If there's a current name remaining, add it to the main name
        if current_name:
            if is_in_parenthesis:
                alternate_names.append("".join(current_name).strip())
            else:
                main_name.append("".join(current_name).strip())

        # Join main names into a single name and append alternate names
        extracted_names = tuple([" ".join(main_name)] + alternate_names)
        result.append(extracted_names)

    return result

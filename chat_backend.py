from search_in_db import product_search
from process_query import clean_sentence,process_query

def is_about_previous_products(entities):
    indices = []
    for entity in entities:
        if entity.isdigit() and int(entity) < 5:
            indices.append(int(entity))
    return indices if indices else None

retrieve_products = True
while True:
    user_input = input("User: ")
    cleaned_query = clean_sentence(user_input)
    if cleaned_query.lower() == "goodbye":
        print("Bot: Goodbye!")
        break

    keywords, entities = process_query(cleaned_query)


    if retrieve_products:
        closest_product_names, closest_other_columns = product_search.get_closest_embeddings_and_rows(keywords.lower(), k=5)
        for idx, products in enumerate(closest_product_names):
            print(f"{idx} {products} \n")
        retrieve_products = False
    else:
        indices = is_about_previous_products(entities)
        if indices:
            for index in indices:
                if 0 <= index < 5:
                    for key, value_list in closest_other_columns.items():
                        print(f"{key}: {value_list[index]}")
                else:
                    print(f"Invalid entity index: {index}")
        else:
            closest_product_names, closest_other_columns = product_search.get_closest_embeddings_and_rows(keywords.lower(), k=5)
            for idx, products in enumerate(closest_product_names):
                print(f"{idx} {products} \n")

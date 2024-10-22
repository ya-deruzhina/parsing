from apps.wb.serializers import CatalogSerializer

def servise_chose_data_product (product_info,data_price,id_product):
    try:        
        name_product = product_info['imt_name']
        type_product = product_info['subj_name']
        root_type_product = product_info['subj_root_name']
        vendor_code = product_info['vendor_code']
        description = product_info['description']
        color = product_info['nm_colors_names']
        contents = product_info['contents']
        brand_name = product_info['selling']['brand_name']

        options = []
        inf_option = product_info['grouped_options']
        for option in inf_option:
            data = f'{option["group_name"]}: {option["options"][0]["name"]} - {option["options"][0]["value"]}'
            options.append(data)
        options = ", ".join(options)

        price_without_nds = float(str(data_price[-1]['price']['RUB'])[:-2])
        price = round(price_without_nds* 1.2328524)
            
        data = {
            "id":id_product,
            "name_product":name_product,
            "type_product":type_product,
            "root_type_product":root_type_product,
            "vendor_code":vendor_code,
            "description":description,
            "color":color,
            "contents":contents,
            "brand_name":brand_name,
            "options":options,
            "price_without_nds":price_without_nds,
            "price":price
        }

        serializer = CatalogSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return(serializer.data)
    except:
        pass
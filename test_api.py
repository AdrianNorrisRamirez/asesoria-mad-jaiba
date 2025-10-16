import requests
import json
import time

# Configuración de la API
BASE_URL = "http://127.0.0.1:5000"

def test_api():
    print("🚀 Iniciando pruebas de la API...")
    
    # Esperar a que el servidor inicie
    time.sleep(2)
    
    # 1. Probar la ruta raíz
    print("\n1. Probando ruta raíz...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # 2. Crear un equipo
    print("\n2. Creando un equipo...")
    equipment_data = {
        "name": "Máquina de Ensamblaje A-1",
        "location": "Planta 1, Sección 3",
        "serial_number": "SN-A1-12345"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/equipment", json=equipment_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            equipment = response.json()
            print(f"   Response: {json.dumps(equipment, indent=2)}")
            equipment_id = equipment.get('id')
            
            # 3. Obtener el equipo creado
            print("\n3. Obteniendo el equipo creado...")
            response = requests.get(f"{BASE_URL}/equipment/{equipment_id}")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            # 4. Crear un producto asociado al equipo
            print("\n4. Creando un producto asociado al equipo...")
            product_data = {
                "name": "Widget Estándar",
                "price": 29.99,
                "description": "Widget estándar para ensamblaje",
                "category": "Componentes"
            }
            
            response = requests.post(f"{BASE_URL}/products", json=product_data)
            print(f"   Status: {response.status_code}")
            if response.status_code == 201:
                product = response.json()
                print(f"   Response: {json.dumps(product, indent=2)}")
                
                # 5. Obtener todos los equipos
                print("\n5. Obteniendo todos los equipos...")
                response = requests.get(f"{BASE_URL}/equipment")
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    equipment_list = response.json()
                    print(f"   Total equipos: {len(equipment_list)}")
                    for eq in equipment_list:
                        print(f"   - {eq['name']} ({eq['id']})")
                
                # 6. Obtener todos los productos
                print("\n6. Obteniendo todos los productos...")
                response = requests.get(f"{BASE_URL}/products")
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    product_list = response.json()
                    print(f"   Total productos: {len(product_list)}")
                    for prod in product_list:
                        print(f"   - {prod['name']} (${prod['price']})")
            
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_api()
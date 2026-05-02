import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from complaints.models import Province, District, Municipality, Ward

print("Seeding Nepal data...")

# =====================
# PROVINCES
# =====================
provinces = [
    {"name": "Koshi Province", "name_np": "कोशी प्रदेश"},
    {"name": "Madhesh Province", "name_np": "मधेश प्रदेश"},
    {"name": "Bagmati Province", "name_np": "बागमती प्रदेश"},
    {"name": "Gandaki Province", "name_np": "गण्डकी प्रदेश"},
    {"name": "Lumbini Province", "name_np": "लुम्बिनी प्रदेश"},
    {"name": "Karnali Province", "name_np": "कर्णाली प्रदेश"},
    {"name": "Sudurpashchim Province", "name_np": "सुदूरपश्चिम प्रदेश"},
]

province_objs = {}
for p in provinces:
    obj, _ = Province.objects.get_or_create(name=p["name"], defaults={"name_np": p["name_np"]})
    province_objs[p["name"]] = obj
    print(f"  ✓ Province: {p['name']}")

# =====================
# DISTRICTS (Major ones)
# =====================
districts = [
    # Koshi
    {"province": "Koshi Province", "name": "Taplejung", "name_np": "ताप्लेजुङ"},
    {"province": "Koshi Province", "name": "Sankhuwasabha", "name_np": "सङ्खुवासभा"},
    {"province": "Koshi Province", "name": "Solukhumbu", "name_np": "सोलुखुम्बु"},
    {"province": "Koshi Province", "name": "Okhaldhunga", "name_np": "ओखलढुङ्गा"},
    {"province": "Koshi Province", "name": "Khotang", "name_np": "खोटाङ"},
    {"province": "Koshi Province", "name": "Bhojpur", "name_np": "भोजपुर"},
    {"province": "Koshi Province", "name": "Dhankuta", "name_np": "धनकुटा"},
    {"province": "Koshi Province", "name": "Terhathum", "name_np": "तेह्रथुम"},
    {"province": "Koshi Province", "name": "Sunsari", "name_np": "सुनसरी"},
    {"province": "Koshi Province", "name": "Morang", "name_np": "मोरङ"},
    {"province": "Koshi Province", "name": "Jhapa", "name_np": "झापा"},
    {"province": "Koshi Province", "name": "Ilam", "name_np": "इलाम"},
    {"province": "Koshi Province", "name": "Panchthar", "name_np": "पाँचथर"},
    {"province": "Koshi Province", "name": "Udayapur", "name_np": "उदयपुर"},
    # Madhesh
    {"province": "Madhesh Province", "name": "Saptari", "name_np": "सप्तरी"},
    {"province": "Madhesh Province", "name": "Siraha", "name_np": "सिरहा"},
    {"province": "Madhesh Province", "name": "Dhanusha", "name_np": "धनुषा"},
    {"province": "Madhesh Province", "name": "Mahottari", "name_np": "महोत्तरी"},
    {"province": "Madhesh Province", "name": "Sarlahi", "name_np": "सर्लाही"},
    {"province": "Madhesh Province", "name": "Rautahat", "name_np": "रौतहट"},
    {"province": "Madhesh Province", "name": "Bara", "name_np": "बारा"},
    {"province": "Madhesh Province", "name": "Parsa", "name_np": "पर्सा"},
    # Bagmati
    {"province": "Bagmati Province", "name": "Kathmandu", "name_np": "काठमाडौँ"},
    {"province": "Bagmati Province", "name": "Bhaktapur", "name_np": "भक्तपुर"},
    {"province": "Bagmati Province", "name": "Lalitpur", "name_np": "ललितपुर"},
    {"province": "Bagmati Province", "name": "Kavrepalanchok", "name_np": "काभ्रेपलाञ्चोक"},
    {"province": "Bagmati Province", "name": "Sindhupalchok", "name_np": "सिन्धुपाल्चोक"},
    {"province": "Bagmati Province", "name": "Rasuwa", "name_np": "रसुवा"},
    {"province": "Bagmati Province", "name": "Nuwakot", "name_np": "नुवाकोट"},
    {"province": "Bagmati Province", "name": "Dhading", "name_np": "धादिङ"},
    {"province": "Bagmati Province", "name": "Makwanpur", "name_np": "मकवानपुर"},
    {"province": "Bagmati Province", "name": "Chitwan", "name_np": "चितवन"},
    {"province": "Bagmati Province", "name": "Sindhuli", "name_np": "सिन्धुली"},
    {"province": "Bagmati Province", "name": "Ramechhap", "name_np": "रामेछाप"},
    {"province": "Bagmati Province", "name": "Dolakha", "name_np": "दोलखा"},
    # Gandaki
    {"province": "Gandaki Province", "name": "Kaski", "name_np": "कास्की"},
    {"province": "Gandaki Province", "name": "Syangja", "name_np": "स्याङ्जा"},
    {"province": "Gandaki Province", "name": "Tanahun", "name_np": "तनहुँ"},
    {"province": "Gandaki Province", "name": "Lamjung", "name_np": "लमजुङ"},
    {"province": "Gandaki Province", "name": "Gorkha", "name_np": "गोर्खा"},
    {"province": "Gandaki Province", "name": "Manang", "name_np": "मनाङ"},
    {"province": "Gandaki Province", "name": "Mustang", "name_np": "मुस्ताङ"},
    {"province": "Gandaki Province", "name": "Myagdi", "name_np": "म्याग्दी"},
    {"province": "Gandaki Province", "name": "Baglung", "name_np": "बाग्लुङ"},
    {"province": "Gandaki Province", "name": "Parbat", "name_np": "पर्वत"},
    {"province": "Gandaki Province", "name": "Nawalpur", "name_np": "नवलपुर"},
    # Lumbini
    {"province": "Lumbini Province", "name": "Rupandehi", "name_np": "रुपन्देही"},
    {"province": "Lumbini Province", "name": "Kapilvastu", "name_np": "कपिलवस्तु"},
    {"province": "Lumbini Province", "name": "Arghakhanchi", "name_np": "अर्घाखाँची"},
    {"province": "Lumbini Province", "name": "Gulmi", "name_np": "गुल्मी"},
    {"province": "Lumbini Province", "name": "Palpa", "name_np": "पाल्पा"},
    {"province": "Lumbini Province", "name": "Nawalparasi", "name_np": "नवलपरासी"},
    {"province": "Lumbini Province", "name": "Rolpa", "name_np": "रोल्पा"},
    {"province": "Lumbini Province", "name": "Pyuthan", "name_np": "प्युठान"},
    {"province": "Lumbini Province", "name": "Dang", "name_np": "दाङ"},
    {"province": "Lumbini Province", "name": "Banke", "name_np": "बाँके"},
    {"province": "Lumbini Province", "name": "Bardiya", "name_np": "बर्दिया"},
    {"province": "Lumbini Province", "name": "Eastern Rukum", "name_np": "पूर्वी रुकुम"},
    # Karnali
    {"province": "Karnali Province", "name": "Dolpa", "name_np": "डोल्पा"},
    {"province": "Karnali Province", "name": "Humla", "name_np": "हुम्ला"},
    {"province": "Karnali Province", "name": "Jumla", "name_np": "जुम्ला"},
    {"province": "Karnali Province", "name": "Kalikot", "name_np": "कालिकोट"},
    {"province": "Karnali Province", "name": "Mugu", "name_np": "मुगु"},
    {"province": "Karnali Province", "name": "Surkhet", "name_np": "सुर्खेत"},
    {"province": "Karnali Province", "name": "Dailekh", "name_np": "दैलेख"},
    {"province": "Karnali Province", "name": "Jajarkot", "name_np": "जाजरकोट"},
    {"province": "Karnali Province", "name": "Western Rukum", "name_np": "पश्चिम रुकुम"},
    {"province": "Karnali Province", "name": "Salyan", "name_np": "सल्यान"},
    # Sudurpashchim
    {"province": "Sudurpashchim Province", "name": "Kanchanpur", "name_np": "कञ्चनपुर"},
    {"province": "Sudurpashchim Province", "name": "Kailali", "name_np": "कैलाली"},
    {"province": "Sudurpashchim Province", "name": "Doti", "name_np": "डोटी"},
    {"province": "Sudurpashchim Province", "name": "Achham", "name_np": "अछाम"},
    {"province": "Sudurpashchim Province", "name": "Bajura", "name_np": "बाजुरा"},
    {"province": "Sudurpashchim Province", "name": "Bajhang", "name_np": "बझाङ"},
    {"province": "Sudurpashchim Province", "name": "Darchula", "name_np": "दार्चुला"},
    {"province": "Sudurpashchim Province", "name": "Baitadi", "name_np": "बैतडी"},
    {"province": "Sudurpashchim Province", "name": "Dadeldhura", "name_np": "डडेलधुरा"},
]

district_objs = {}
for d in districts:
    obj, _ = District.objects.get_or_create(
        name=d["name"],
        defaults={
            "name_np": d["name_np"],
            "province": province_objs[d["province"]]
        }
    )
    district_objs[d["name"]] = obj
    print(f"  ✓ District: {d['name']}")

# =====================
# MUNICIPALITIES (Major ones)
# =====================
municipalities = [
    # Kathmandu
    {"district": "Kathmandu", "name": "Kathmandu Metropolitan City", "name_np": "काठमाडौँ महानगरपालिका", "type": "metropolitan", "total_wards": 32},
    {"district": "Kathmandu", "name": "Kirtipur Municipality", "name_np": "कीर्तिपुर नगरपालिका", "type": "municipality", "total_wards": 10},
    {"district": "Kathmandu", "name": "Budhanilkantha Municipality", "name_np": "बुढानीलकण्ठ नगरपालिका", "type": "municipality", "total_wards": 13},
    {"district": "Kathmandu", "name": "Kageshwori Manohara Municipality", "name_np": "कागेश्वरी मनोहरा नगरपालिका", "type": "municipality", "total_wards": 9},
    {"district": "Kathmandu", "name": "Gokarneshwor Municipality", "name_np": "गोकर्णेश्वर नगरपालिका", "type": "municipality", "total_wards": 9},
    {"district": "Kathmandu", "name": "Tarakeshwor Municipality", "name_np": "तारकेश्वर नगरपालिका", "type": "municipality", "total_wards": 11},
    {"district": "Kathmandu", "name": "Tokha Municipality", "name_np": "टोखा नगरपालिका", "type": "municipality", "total_wards": 11},
    {"district": "Kathmandu", "name": "Chandragiri Municipality", "name_np": "चन्द्रागिरि नगरपालिका", "type": "municipality", "total_wards": 15},
    {"district": "Kathmandu", "name": "Dakshinkali Municipality", "name_np": "दक्षिणकाली नगरपालिका", "type": "municipality", "total_wards": 11},
    {"district": "Kathmandu", "name": "Nagarjun Municipality", "name_np": "नागार्जुन नगरपालिका", "type": "municipality", "total_wards": 10},
    {"district": "Kathmandu", "name": "Shankharapur Municipality", "name_np": "शङ्खरापुर नगरपालिका", "type": "municipality", "total_wards": 9},
    # Lalitpur
    {"district": "Lalitpur", "name": "Lalitpur Metropolitan City", "name_np": "ललितपुर महानगरपालिका", "type": "metropolitan", "total_wards": 29},
    {"district": "Lalitpur", "name": "Godawari Municipality", "name_np": "गोदावरी नगरपालिका", "type": "municipality", "total_wards": 14},
    {"district": "Lalitpur", "name": "Mahalaxmi Municipality", "name_np": "महालक्ष्मी नगरपालिका", "type": "municipality", "total_wards": 11},
    # Bhaktapur
    {"district": "Bhaktapur", "name": "Bhaktapur Municipality", "name_np": "भक्तपुर नगरपालिका", "type": "municipality", "total_wards": 10},
    {"district": "Bhaktapur", "name": "Madhyapur Thimi Municipality", "name_np": "मध्यपुर थिमि नगरपालिका", "type": "municipality", "total_wards": 7},
    {"district": "Bhaktapur", "name": "Changunarayan Municipality", "name_np": "चाँगुनारायण नगरपालिका", "type": "municipality", "total_wards": 9},
    {"district": "Bhaktapur", "name": "Suryabinayak Municipality", "name_np": "सूर्यबिनायक नगरपालिका", "type": "municipality", "total_wards": 8},
    # Kaski
    {"district": "Kaski", "name": "Pokhara Metropolitan City", "name_np": "पोखरा महानगरपालिका", "type": "metropolitan", "total_wards": 33},
    # Chitwan
    {"district": "Chitwan", "name": "Bharatpur Metropolitan City", "name_np": "भरतपुर महानगरपालिका", "type": "metropolitan", "total_wards": 29},
    {"district": "Chitwan", "name": "Ratnanagar Municipality", "name_np": "रत्ननगर नगरपालिका", "type": "municipality", "total_wards": 14},
    # Rupandehi
    {"district": "Rupandehi", "name": "Butwal Sub-Metropolitan City", "name_np": "बुटवल उपमहानगरपालिका", "type": "sub_metropolitan", "total_wards": 19},
    {"district": "Rupandehi", "name": "Siddharthanagar Municipality", "name_np": "सिद्धार्थनगर नगरपालिका", "type": "municipality", "total_wards": 17},
    # Morang
    {"district": "Morang", "name": "Biratnagar Metropolitan City", "name_np": "विराटनगर महानगरपालिका", "type": "metropolitan", "total_wards": 19},
    {"district": "Morang", "name": "Urlabari Municipality", "name_np": "उर्लाबारी नगरपालिका", "type": "municipality", "total_wards": 9},
    # Sunsari
    {"district": "Sunsari", "name": "Dharan Sub-Metropolitan City", "name_np": "धरान उपमहानगरपालिका", "type": "sub_metropolitan", "total_wards": 19},
    {"district": "Sunsari", "name": "Inaruwa Municipality", "name_np": "इनरुवा नगरपालिका", "type": "municipality", "total_wards": 9},
    # Jhapa
    {"district": "Jhapa", "name": "Mechinagar Municipality", "name_np": "मेची नगर नगरपालिका", "type": "municipality", "total_wards": 9},
    {"district": "Jhapa", "name": "Birtamode Municipality", "name_np": "बिर्तामोड नगरपालिका", "type": "municipality", "total_wards": 9},
    # Banke
    {"district": "Banke", "name": "Nepalgunj Sub-Metropolitan City", "name_np": "नेपालगञ्ज उपमहानगरपालिका", "type": "sub_metropolitan", "total_wards": 18},
    # Kailali
    {"district": "Kailali", "name": "Dhangadhi Sub-Metropolitan City", "name_np": "धनगढी उपमहानगरपालिका", "type": "sub_metropolitan", "total_wards": 19},
    # Kanchanpur
    {"district": "Kanchanpur", "name": "Bhimdatta Municipality", "name_np": "भीमदत्त नगरपालिका", "type": "municipality", "total_wards": 16},
    # Surkhet
    {"district": "Surkhet", "name": "Birendranagar Municipality", "name_np": "वीरेन्द्रनगर नगरपालिका", "type": "municipality", "total_wards": 11},
    # Bara
    {"district": "Bara", "name": "Kalaiya Sub-Metropolitan City", "name_np": "कलैया उपमहानगरपालिका", "type": "sub_metropolitan", "total_wards": 16},
    # Parsa
    {"district": "Parsa", "name": "Birgunj Metropolitan City", "name_np": "वीरगञ्ज महानगरपालिका", "type": "metropolitan", "total_wards": 32},
    # Dhanusha
    {"district": "Dhanusha", "name": "Janakpur Sub-Metropolitan City", "name_np": "जनकपुर उपमहानगरपालिका", "type": "sub_metropolitan", "total_wards": 17},
]

muni_objs = {}
for m in municipalities:
    obj, _ = Municipality.objects.get_or_create(
        name=m["name"],
        defaults={
            "name_np": m["name_np"],
            "type": m["type"],
            "total_wards": m["total_wards"],
            "district": district_objs[m["district"]]
        }
    )
    muni_objs[m["name"]] = obj
    print(f"  ✓ Municipality: {m['name']}")

# =====================
# WARDS — Auto generate
# =====================
print("\nGenerating wards...")
for muni_name, muni_obj in muni_objs.items():
    for i in range(1, muni_obj.total_wards + 1):
        Ward.objects.get_or_create(
            municipality=muni_obj,
            ward_number=i
        )
    print(f"  ✓ {muni_name} — {muni_obj.total_wards} wards")

print("\n✅ Seed complete!")
print(f"   Provinces: {Province.objects.count()}")
print(f"   Districts: {District.objects.count()}")
print(f"   Municipalities: {Municipality.objects.count()}")
print(f"   Wards: {Ward.objects.count()}")
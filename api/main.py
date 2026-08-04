webhook os
import random
from flask import Flask, request, Response
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Token bot dari environment variable
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN / TOKEN environment variable is required")

# Daftar ramalan masa depan (100+)
RAMALAN = [
    "pengusaha sukses",
    "orang kaya",
    "gembel",
    "programmer terkenal",
    "CEO startup",
    "dokter",
    "pilot",
    "polisi",
    "tentara",
    "presiden",
    "menteri",
    "youtuber sukses",
    "streamer terkenal",
    "gamer profesional",
    "influencer",
    "konten kreator",
    "miliarder",
    "investor saham",
    "trader sukses",
    "trader yang sering MC",
    "raja meme",
    "tukang bakso",
    "tukang parkir",
    "penjual gorengan",
    "penjual kopi",
    "bos perusahaan",
    "peternak sukses",
    "pemilik restoran",
    "pemilik hotel",
    "sultan",
    "raja crypto",
    "kolektor mobil mewah",
    "hidup sederhana tapi bahagia",
    "menikah muda",
    "jomblo seumur hidup",
    "punya 10 kucing",
    "keliling dunia",
    "tinggal di luar negeri",
    "jadi orang terkenal",
    "jadi orang misterius",
    "artis sinetron",
    "penyanyi terkenal",
    "penulis best seller",
    "ilmuwan genial",
    "astronaut",
    "nelayan sukses",
    "petani modern",
    "desainer fashion",
    "arsitek terkenal",
    "chef bintang lima",
    "barista legendaris",
    "driver ojek online legendaris",
    "pemilik warnet",
    "bos rental mobil",
    "penjual es krim keliling",
    "tukang cukur terkenal",
    "montir motor legendaris",
    "guru favorit murid",
    "dosen yang disegani",
    "psikolog sukses",
    "pengacara handal",
    "hakim yang adil",
    "notaris ternama",
    "bankir top",
    "akuntan berpengalaman",
    "marketing genius",
    "sales legendaris",
    "HRD yang dicintai karyawan",
    "manajer proyek sukses",
    "konsultan bisnis",
    "motivator nasional",
    "pembicara TED Talk",
    "podcaster populer",
    "tiktoker viral",
    "reels king/queen",
    "photographer profesional",
    "videographer terkenal",
    "editor film",
    "sutradara blockbuster",
    "aktor Hollywood",
    "model internasional",
    "atlit olimpiade",
    "pelatih sepak bola legenda",
    "pemain esports juara dunia",
    "streamer yang full time",
    "moderator komunitas besar",
    "admin grup paling aktif",
    "raja giveaway",
    "kolektor NFT",
    "trader forex yang disiplin",
    "pemilik kafe aesthetic",
    "bos laundry kiloan",
    "penjual bubur ayam legendaris",
    "tukang sate madura terkenal",
    "pemilik toko kelontong modern",
    "agen properti sukses",
    "makelar tanah tajir",
    "peternak lele sukses",
    "peternak ayam petelur",
    "pemilik kebun hidroponik",
    "raja tanaman hias",
    "kolektor jam tangan mewah",
    "pemilik yacht",
    "pilot drone profesional",
    "ahli cybersecurity",
    "ethical hacker terkenal",
    "data scientist top",
    "AI engineer",
    "robotics engineer",
    "game developer indie sukses",
    "mobile app developer terkenal",
    "web developer full stack legenda",
    "UI/UX designer favorit",
    "product manager di unicorn",
    "founder unicorn startup",
    "angel investor",
    "venture capitalist",
    "pemilik franchise makanan",
    "raja franchise kopi",
    "bos franchise laundry",
    "pemilik gym terkenal",
    "personal trainer seleb",
    "nutritionist terkenal",
    "life coach inspiratif",
    "public speaker internasional",
    "penulis buku self-help",
    "novelis best seller",
    "penyair modern",
    "komikus viral",
    "ilustrator terkenal",
    "animator studio besar",
    "vlogger travel",
    "food blogger legenda",
    "beauty influencer",
    "fashion influencer",
    "tech reviewer",
    "gadget unboxing king",
    "pemilik toko online besar",
    "dropshipper sukses",
    "affiliate marketing king",
    "SEO specialist top",
    "digital marketer handal",
    "social media manager seleb",
    "community manager besar",
    "customer success hero",
    "support agent legenda",
    "devops engineer",
    "cloud architect",
    "blockchain developer",
    "smart contract auditor",
    "metaverse builder",
    "VR/AR developer",
    "quantum computing researcher",
    "biotech scientist",
    "climate activist terkenal",
    "environmentalist inspiratif",
    "volunteer internasional",
    "humanitarian worker",
    "diplomat",
    "ambassador",
    "senator",
    "gubernur",
    "walikota favorit rakyat",
    "bupati yang dicintai",
    "camat paling ramah",
    "lurah legenda",
    "RT paling aktif",
    "RW yang disegani",
    "ketua RT yang selalu hadir",
    "pemilik kos-kosan full booked",
    "bos kontrakan",
    "pemilik apartemen",
    "investor properti",
    "raja tanah",
    "pemilik sawah luas",
    "petani organik sukses",
    "nelayan modern dengan kapal besar",
    "pemilik kapal pesiar",
    "captain kapal kargo",
    "pramugari/pramugara",
    "ground handling staff legenda",
    "mekanik pesawat",
    "air traffic controller",
    "meteorologist",
    "ahli gempa",
    "vulkanolog",
    "peneliti antariksa",
    "astronom amatir terkenal",
    "astrofotografer",
    "stargazer professional",
    "pemilik observatorium pribadi",
    "kolektor bintang jatuh (figuratif)",
    "hidup bahagia tanpa target",
    "jadi orang yang selalu bersyukur",
    "punya banyak sahabat sejati",
    "menjadi mentor generasi muda",
    "jadi panutan keluarga",
    "hidup tenang di desa",
    "jadi petani digital",
    "punya kebun buah sendiri",
    "jadi pemilik restoran seafood",
    "raja sate padang",
    "penjual martabak legenda",
    "bos warung kopi 24 jam",
    "pemilik toko buku independen",
    "kolektor komik langka",
    "pemilik board game cafe",
    "raja event organizer",
    "wedding organizer top",
    "fotografer prewedding favorit",
    "makeup artist seleb",
    "hair stylist terkenal",
    "spa owner sukses",
    "yoga instructor inspiratif",
    "meditation teacher",
    "spiritual guide",
    "jadi orang yang selalu positif",
    "hidup minimalis tapi kaya pengalaman",
    "jadi digital nomad",
    "kerja remote sambil keliling dunia",
    "punya rumah di pantai",
    "punya cabin di pegunungan",
    "jadi orang yang paling sering ketawa",
    "jadi sumber kebahagiaan orang lain",
]

app = Flask(__name__)

# Build Application (updater=None karena kita handle webhook manual)
application = (
    Application.builder()
    .token(TOKEN)
    .updater(None)
    .build()
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Selamat datang di Bot Ramalan Masa Depan!\n\n"
        "Bot ini hanya untuk hiburan. Semua ramalan bersifat acak dan tidak benar-benar memprediksi masa depanmu.\n\n"
        "Ketik /masadepanku untuk melihat ramalan masa depanmu 🔮\n"
        "Ketik /help untuk melihat daftar perintah."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📋 Daftar Perintah:\n\n"
        "/start - Pesan selamat datang\n"
        "/help - Menampilkan bantuan ini\n"
        "/masadepanku - Melihat ramalan masa depan secara acak 🔮\n\n"
        "⚠️ Semua ramalan hanya untuk hiburan!"
    )


async def masadepanku(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ramalan = random.choice(RAMALAN)
    await update.message.reply_text(
        f"🔮 Melihat masa depanmu...\n\n"
        f"✨ Masa depanmu akan menjadi {ramalan}."
    )


# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("masadepanku", masadepanku))


@app.route("/", methods=["GET"])
def index():
    return "Bot Ramalan Masa Depan is running! 🔮", 200


@app.route("/", methods=["POST"])
async def webhook():
    """Handle incoming Telegram updates (Vercel / webhook mode)."""
    if request.headers.get("content-type") == "application/json":
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        async with application:
            await application.process_update(update)
        return Response(status=200)
    return Response(status=403)


def main() -> None:
    """Jalankan bot secara lokal dengan polling."""
    print("Bot berjalan dengan polling (mode lokal)...")
    # Rebuild dengan updater default untuk polling
    polling_app = Application.builder().token(TOKEN).build()
    polling_app.add_handler(CommandHandler("start", start))
    polling_app.add_handler(CommandHandler("help", help_command))
    polling_app.add_handler(CommandHandler("masadepanku", masadepanku))
    polling_app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

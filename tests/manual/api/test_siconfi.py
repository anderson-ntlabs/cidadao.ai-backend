"""
Test SICONFI API - Tesouro Nacional

Tests fiscal and accounting data access for Brazilian municipalities.

Author: Anderson Henrique da Silva
Created: 2025-11-14
License: MIT
"""

import asyncio

from src.services.transparency_apis.federal_apis.siconfi_client import SICONFIClient

# Major municipalities IBGE codes
MUNICIPALITIES = {
    "São Paulo": "3550308",
    "Rio de Janeiro": "3304557",
    "Brasília": "5300108",
    "Belo Horizonte": "3106200",
    "Salvador": "2927408",
    "Fortaleza": "2304400",
    "Recife": "2611606",
    "Porto Alegre": "4314902",
}


async def test_siconfi():
    print("=" * 80)
    print("Testing SICONFI API - Tesouro Nacional")
    print("=" * 80)
    print()

    results = {}

    async with SICONFIClient() as client:
        # Test 1: Get entities list
        print("1. Testing entities list...")
        try:
            entities = await client.get_entities(year=2024, sphere="M", state="SP")
            results["entities"] = f"✅ {len(entities)} municipalities in SP"
            print(f"   ✅ Found {len(entities)} municipalities in São Paulo state")
        except Exception as e:
            results["entities"] = f"❌ {str(e)[:60]}"
            print(f"   ❌ Error: {str(e)[:60]}")

        print()

        # Test 2-4: Test RREO, RGF, DCA for São Paulo
        city = "São Paulo"
        code = MUNICIPALITIES[city]

        print(f"2. Testing RREO (Budget Execution) for {city}...")
        try:
            rreo = await client.get_rreo(
                year=2024, period=1, entity_code=code, limit=10
            )
            results["rreo"] = f"✅ {len(rreo)} records"
            print(f"   ✅ Found {len(rreo)} budget execution records")
            if rreo:
                print(f"   Sample: {rreo[0].ente} - {rreo[0].anexo}")
        except Exception as e:
            results["rreo"] = f"❌ {str(e)[:60]}"
            print(f"   ❌ Error: {str(e)[:60]}")

        print()

        print(f"3. Testing RGF (Fiscal Management) for {city}...")
        try:
            rgf = await client.get_rgf(year=2024, period=1, entity_code=code, limit=10)
            results["rgf"] = f"✅ {len(rgf)} records"
            print(f"   ✅ Found {len(rgf)} fiscal management records")
            if rgf:
                print(f"   Sample: {rgf[0].ente} - {rgf[0].anexo}")
        except Exception as e:
            results["rgf"] = f"❌ {str(e)[:60]}"
            print(f"   ❌ Error: {str(e)[:60]}")

        print()

        print(f"4. Testing DCA (Annual Accounts) for {city}...")
        try:
            dca = await client.get_dca(year=2023, entity_code=code, limit=10)
            results["dca"] = f"✅ {len(dca)} records"
            print(f"   ✅ Found {len(dca)} annual account records")
            if dca:
                print(f"   Sample: {dca[0].ente} - {dca[0].anexo}")
        except Exception as e:
            results["dca"] = f"❌ {str(e)[:60]}"
            print(f"   ❌ Error: {str(e)[:60]}")

        print()

        print(f"5. Testing MSC (Accounting Balances) for {city}...")
        try:
            msc = await client.get_msc(year=2024, month=1, entity_code=code, limit=10)
            results["msc"] = f"✅ {len(msc)} records"
            print(f"   ✅ Found {len(msc)} accounting balance records")
            if msc:
                print(f"   Sample: {msc[0].ente} - Account {msc[0].conta_contabil}")
        except Exception as e:
            results["msc"] = f"❌ {str(e)[:60]}"
            print(f"   ❌ Error: {str(e)[:60]}")

        print()

        # Test 6: Complete summary for a municipality
        print(f"6. Testing complete summary for {city}...")
        try:
            summary = await client.get_municipality_summary(entity_code=code, year=2023)
            results["summary"] = f"✅ {summary['total_records']} total records"
            print("   ✅ Complete summary retrieved:")
            print(
                f"      - Budget execution: {len(summary['budget_execution'])} records"
            )
            print(
                f"      - Fiscal management: {len(summary['fiscal_management'])} records"
            )
            print(f"      - Annual accounts: {len(summary['annual_accounts'])} records")
            print(f"      - Total: {summary['total_records']} records")
        except Exception as e:
            results["summary"] = f"❌ {str(e)[:60]}"
            print(f"   ❌ Error: {str(e)[:60]}")

        print()

        # Test 7: Test multiple municipalities
        print("7. Testing multiple major municipalities...")
        successful = 0
        failed = 0
        for city_name, city_code in list(MUNICIPALITIES.items())[:5]:
            try:
                rreo = await client.get_rreo(
                    year=2023, period=6, entity_code=city_code, limit=5
                )
                if rreo:
                    print(f"   ✅ {city_name:20} - {len(rreo)} records")
                    successful += 1
                else:
                    print(f"   ⚠️  {city_name:20} - No data available")
                    failed += 1
            except Exception as e:
                print(f"   ❌ {city_name:20} - {str(e)[:40]}")
                failed += 1

        results["multiple_cities"] = f"✅ {successful}/{successful+failed} cities"

    # Summary
    print()
    print("=" * 80)
    print("SUMMARY - SICONFI API TEST")
    print("=" * 80)
    print()

    for test, status in results.items():
        print(f"   {test:20} {status}")

    print()

    working = sum(1 for r in results.values() if "✅" in r)
    total = len(results)

    print(f"✅ Working: {working}/{total} ({working/total*100:.1f}%)")
    print()

    if working == total:
        print("🎉 All SICONFI endpoints working perfectly!")
    elif working > total / 2:
        print("✅ SICONFI integration mostly functional")
    else:
        print("⚠️  SICONFI integration needs investigation")

    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_siconfi())

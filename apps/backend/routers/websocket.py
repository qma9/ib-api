from fastapi import APIRouter, WebSocket
from ib_insync import IB, Forex, util

# Create a new APIRouter instance
router = APIRouter()
# Create a new IB instance
ib = IB()

@router.websocket("/")  # /ws/market_data
async def market_data_endpoint(websocket: WebSocket):
    """
    Websocket endpoint for market data
    """
    await websocket.accept()
    try:
        ib.connect('127.0.0.1', 7497, clientId=1)  # Connect to the Interactive Brokers API
        contract = Forex('EURUSD')

        while True:
            bars = ib.reqHistoricalData(
                contract, endDateTime='', durationStr='30 D',
                barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True
            )
            df_bars = util.df(bars)  # Convert bars to DataFrame
            await websocket.send_text(f"Market data for {contract.symbol}: {df_bars.to_string()}")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
        await websocket.close()
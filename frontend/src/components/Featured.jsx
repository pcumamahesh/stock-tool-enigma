import React from 'react'
import TrendCard from './TrendCard'
import '../styles/Featured.css'

function Featured() {
    return (
        <div className='parent'>
            <h1>Featured</h1>
            <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', marginTop: '20px' }}>
                <TrendCard
                    icon="https://example.com/company-icon1.png"
                    name="Company A"
                    price="123.45"
                    trend="Uptrend"
                />
                <TrendCard
                    icon="https://example.com/company-icon2.png"
                    name="Company B"
                    price="98.76"
                    trend="Downtrend"
                />
                <TrendCard
                    icon="https://example.com/company-icon3.png"
                    name="Company C"
                    price="150.00"
                    trend="Neutral"
                />
            </div>
        </div>
    )
}

export default Featured
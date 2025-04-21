import Image from "next/image"
import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white overflow-x-hidden">
      {/* Background with space theme */}
      <div className="absolute inset-0 z-0 overflow-hidden">
        <Image src="/space-background.png" alt="Space background" fill className="object-cover opacity-80" priority />
      </div>

      {/* Header */}
      <header className="relative z-10 flex items-center justify-between p-4 md:p-6">
        <div className="flex items-center gap-2">
          <Image src="/logo.png" alt="Launchpad Logo" width={28} height={28} />
          <span className="text-lg font-medium border-b-2 border-[#9aabf1]">Launchpad</span>
        </div>
        <div className="flex items-center gap-4">
          <button className="md:hidden">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="text-white"
            >
              <line x1="3" y1="12" x2="21" y2="12"></line>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
          </button>
          <Button className="bg-transparent border border-white rounded-full px-6 hover:bg-white/10">connect</Button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative z-10 px-4 pt-16 md:pt-24 pb-12 md:pb-20 max-w-6xl mx-auto">
        <div className="max-w-3xl">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-4">
            The Decentralized,
            <br />
            Multi-Project Platform
          </h1>
          <p className="text-sm md:text-base opacity-90 mb-8 max-w-2xl">
            A comprehensive platform enabling developers to deploy their projects seamlessly and allowing users to
            engage with these projects securely.
          </p>

          <div className="flex flex-wrap gap-4 mb-12">
            <Button className="bg-transparent border border-white rounded-full px-6 hover:bg-white/10">
              IDO POOLS
            </Button>
            <Button className="bg-transparent border border-white rounded-full px-6 hover:bg-white/10">
              STAKE SYOTX
            </Button>
            <Button className="bg-transparent border border-white rounded-full px-6 hover:bg-white/10">
              GET NOTIFIED
            </Button>
          </div>

          <div>
            <p className="text-xs text-gray-400 mb-2">Supported Chains</p>
            <div className="flex items-center gap-4 border-b border-[#9aabf1] pb-2 max-w-xs">
              <Image src="/chain-icon-1.png" alt="Chain" width={20} height={20} />
              <Image src="/chain-icon-2.png" alt="Chain" width={20} height={20} />
              <Image src="/chain-icon-3.png" alt="Chain" width={20} height={20} />
              <Image src="/chain-icon-4.png" alt="Chain" width={20} height={20} />
              <Image src="/chain-icon-5.png" alt="Chain" width={20} height={20} />
              <Image src="/chain-icon-6.png" alt="Chain" width={20} height={20} />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="relative z-10 px-4 py-12 max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Feature 1 */}
          <div className="flex flex-col items-center text-center">
            <div className="mb-4">
              <Image src="/kyc-icon.png" alt="KYC" width={120} height={120} />
            </div>
            <h3 className="text-xl font-semibold mb-2">Sign-Up and KYC</h3>
            <p className="text-sm opacity-80 mb-4">
              To participate in VORTEX Pool, you need to sign up and complete the verification process.
            </p>
            <Button className="bg-transparent border border-white rounded-full px-8 mt-auto hover:bg-white/10">
              SIGN UP
            </Button>
          </div>

          {/* Feature 2 */}
          <div className="flex flex-col items-center text-center">
            <div className="mb-4">
              <Image src="/wallet-icon.png" alt="Wallet" width={120} height={120} />
            </div>
            <h3 className="text-xl font-semibold mb-2">Verify Wallet</h3>
            <p className="text-sm opacity-80 mb-4">
              Upon registration, confirm your wallet address for IDOs. Choose carefully, as each user can verify only
              one wallet.
            </p>
            <Button className="bg-transparent border border-white rounded-full px-8 mt-auto hover:bg-white/10">
              VERIFY
            </Button>
          </div>

          {/* Feature 3 */}
          <div className="flex flex-col items-center text-center">
            <div className="mb-4">
              <Image src="/stake-icon.png" alt="Stake" width={120} height={120} />
            </div>
            <h3 className="text-xl font-semibold mb-2">Stake SYOTX</h3>
            <p className="text-sm opacity-80 mb-4">
              Unlock your tier, increase your multiplier, and secure your allocations by staking SYOTX!
            </p>
            <Button className="bg-transparent border border-white rounded-full px-8 mt-auto hover:bg-white/10">
              STAKE
            </Button>
          </div>

          {/* Feature 4 */}
          <div className="flex flex-col items-center text-center">
            <div className="mb-4">
              <Image src="/register-icon.png" alt="Register" width={120} height={120} />
            </div>
            <h3 className="text-xl font-semibold mb-2">Register for IDOs</h3>
            <p className="text-sm opacity-80 mb-4">
              Sign up for the projects you want to join; only registered participants can take part.
            </p>
            <Button className="bg-transparent border border-white rounded-full px-8 mt-auto hover:bg-white/10">
              REGISTER
            </Button>
          </div>
        </div>
      </section>

      {/* Token Sale Section */}
      <section className="relative z-10 px-4 py-12 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold mb-2">Token Sale Launchpad</h2>
        <p className="text-sm opacity-80 mb-8">
          Secure early access to public and exclusive token sales at a reduced price, before they become available on
          the market.
        </p>

        {/* Tabs */}
        <div className="mb-8">
          <div className="inline-flex border-b border-[#9aabf1]">
            <button className="px-4 py-2 font-medium border-b-2 border-white">Upcoming</button>
          </div>
        </div>

        {/* Upcoming Sales */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {/* Sale 1 */}
          <div className="bg-black/40 border border-[#9aabf1]/30 rounded-lg overflow-hidden">
            <div className="p-4 bg-white/5">
              <Image
                src="/pudgy-penguins.png"
                alt="Pudgy Penguins"
                width={300}
                height={150}
                className="w-full h-auto rounded"
              />
            </div>
            <div className="p-4">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Image src="/pudgy-icon.png" alt="Pudgy" width={24} height={24} />
                  <span>Pudgy Penguins</span>
                </div>
                <button>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <line x1="4" y1="12" x2="20" y2="12"></line>
                    <line x1="4" y1="6" x2="20" y2="6"></line>
                    <line x1="4" y1="18" x2="20" y2="18"></line>
                  </svg>
                </button>
              </div>

              <div className="grid grid-cols-2 gap-2 text-sm mb-4">
                <div>
                  <div className="text-gray-400">Total Raise</div>
                  <div>$100,000</div>
                </div>
                <div>
                  <div className="text-gray-400">Token Price</div>
                  <div>$0.001</div>
                </div>
                <div>
                  <div className="text-gray-400">Start date</div>
                  <div>4/26/2023 11:00</div>
                </div>
                <div>
                  <div className="text-gray-400">Refund Term</div>
                  <div>24 hours</div>
                </div>
                <div>
                  <div className="text-gray-400">Type</div>
                  <div>standard IDO</div>
                </div>
                <div>
                  <div className="text-gray-400">Market Maker</div>
                  <div>Igloo Brand</div>
                </div>
              </div>

              <div className="text-center text-sm text-[#9aabf1]">Registration ends in 06 days</div>
            </div>
          </div>

          {/* Sale 2 */}
          <div className="bg-black/40 border border-[#9aabf1]/30 rounded-lg overflow-hidden">
            <div className="p-4 bg-white/5">
              <Image src="/pepe.png" alt="Pepe" width={300} height={150} className="w-full h-auto rounded" />
            </div>
            <div className="p-4">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Image src="/pepe-icon.png" alt="Pepe" width={24} height={24} />
                  <span>Pepe</span>
                </div>
                <div className="flex items-center">
                  <Image src="/ethereum-icon.png" alt="Ethereum" width={16} height={16} />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-sm mb-4">
                <div>
                  <div className="text-gray-400">Total Raise</div>
                  <div>$100,000</div>
                </div>
                <div>
                  <div className="text-gray-400">Token Price</div>
                  <div>$0.1</div>
                </div>
                <div>
                  <div className="text-gray-400">Start date</div>
                  <div>4/28/2023 17:00</div>
                </div>
                <div>
                  <div className="text-gray-400">Refund Term</div>
                  <div>24 hours</div>
                </div>
                <div>
                  <div className="text-gray-400">Type</div>
                  <div>standard IDO</div>
                </div>
                <div>
                  <div className="text-gray-400">Market Maker</div>
                  <div>Ethereum</div>
                </div>
              </div>

              <div className="text-center">
                <Button className="bg-transparent border border-white/20 rounded-md w-full hover:bg-white/10">
                  TBD
                </Button>
              </div>
            </div>
          </div>

          {/* Sale 3 */}
          <div className="bg-black/40 border border-[#9aabf1]/30 rounded-lg overflow-hidden">
            <div className="p-4 bg-white/5">
              <Image src="/brett.png" alt="Brett" width={300} height={150} className="w-full h-auto rounded" />
            </div>
            <div className="p-4">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Image src="/brett-icon.png" alt="Brett" width={24} height={24} />
                  <span>Brett</span>
                </div>
                <div className="flex items-center">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <circle cx="12" cy="12" r="10"></circle>
                  </svg>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-sm mb-4">
                <div>
                  <div className="text-gray-400">Total Raise</div>
                  <div>$100,000</div>
                </div>
                <div>
                  <div className="text-gray-400">Token Price</div>
                  <div>-</div>
                </div>
                <div>
                  <div className="text-gray-400">Start date</div>
                  <div>6/16/2023 14:00</div>
                </div>
                <div>
                  <div className="text-gray-400">Refund Term</div>
                  <div>24 hours</div>
                </div>
                <div>
                  <div className="text-gray-400">Type</div>
                  <div>standard IDO</div>
                </div>
                <div>
                  <div className="text-gray-400">Market Maker</div>
                  <div>Ethereum</div>
                </div>
              </div>

              <div className="text-center">
                <Button className="bg-transparent border border-white/20 rounded-md w-full hover:bg-white/10">
                  TBD
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Completed Sales */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold">Completed Sales</h3>
            <div className="relative">
              <input
                type="text"
                placeholder="Search by pool name, token symbol"
                className="bg-transparent border border-white/20 rounded-full px-10 py-2 text-sm w-64"
              />
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="absolute left-3 top-1/2 transform -translate-y-1/2"
              >
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </div>
          </div>

          {/* Sales Table */}
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="text-left text-sm text-gray-400">
                  <th className="pb-4 font-normal"></th>
                  <th className="pb-4 font-normal">Total Raise</th>
                  <th className="pb-4 font-normal">Participants</th>
                  <th className="pb-4 font-normal">Current Price</th>
                  <th className="pb-4 font-normal">ATH ROI</th>
                  <th className="pb-4 font-normal">TYPE</th>
                  <th className="pb-4 font-normal">Market Maker</th>
                </tr>
              </thead>
              <tbody>
                {/* Row 1 */}
                <tr className="border-t border-white/10">
                  <td className="py-4">
                    <div className="flex items-center gap-2">
                      <Image src="/bonk-icon.png" alt="Bonk" width={32} height={32} />
                      <div>
                        <div className="flex items-center gap-2">
                          <span>Bonk</span>
                          <span className="text-xs px-2 py-0.5 bg-white/10 rounded-full">Standard IDO</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-4">$100,000</td>
                  <td className="py-4">721</td>
                  <td className="py-4">0.02</td>
                  <td className="py-4">7.2X</td>
                  <td className="py-4">Standard IDO</td>
                  <td className="py-4">None</td>
                </tr>

                {/* Row 2 */}
                <tr className="border-t border-white/10">
                  <td className="py-4">
                    <div className="flex items-center gap-2">
                      <Image src="/toshi-icon.png" alt="Toshi" width={32} height={32} />
                      <div>
                        <div className="flex items-center gap-2">
                          <span>Toshi</span>
                          <span className="text-xs px-2 py-0.5 bg-white/10 rounded-full">Exclusive IDO</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-4">$210,000</td>
                  <td className="py-4">375</td>
                  <td className="py-4">0.1</td>
                  <td className="py-4">4.7X</td>
                  <td className="py-4">Exclusive IDO</td>
                  <td className="py-4">Base</td>
                </tr>

                {/* Row 3 */}
                <tr className="border-t border-white/10">
                  <td className="py-4">
                    <div className="flex items-center gap-2">
                      <Image src="/trump-icon.png" alt="Trump" width={32} height={32} />
                      <div>
                        <div className="flex items-center gap-2">
                          <span>Trump</span>
                          <span className="text-xs px-2 py-0.5 bg-white/10 rounded-full">Standard IDO</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-4">$300,000</td>
                  <td className="py-4">540</td>
                  <td className="py-4">0.005</td>
                  <td className="py-4">6X</td>
                  <td className="py-4">Standard IDO</td>
                  <td className="py-4">None</td>
                </tr>

                {/* Row 4 */}
                <tr className="border-t border-white/10">
                  <td className="py-4">
                    <div className="flex items-center gap-2">
                      <Image src="/freysa-icon.png" alt="Freysa" width={32} height={32} />
                      <div>
                        <div className="flex items-center gap-2">
                          <span>Freysa</span>
                          <span className="text-xs px-2 py-0.5 bg-white/10 rounded-full">Standard IDO</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-4">$550,000</td>
                  <td className="py-4">932</td>
                  <td className="py-4">1.23</td>
                  <td className="py-4">2.5X</td>
                  <td className="py-4">Standard IDO</td>
                  <td className="py-4">Baby Doge</td>
                </tr>

                {/* Row 5 */}
                <tr className="border-t border-white/10">
                  <td className="py-4">
                    <div className="flex items-center gap-2">
                      <Image src="/sensay-icon.png" alt="Sensay" width={32} height={32} />
                      <div>
                        <div className="flex items-center gap-2">
                          <span>Sensay</span>
                          <span className="text-xs px-2 py-0.5 bg-white/10 rounded-full">Exclusive IDO</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-4">$1,100,000</td>
                  <td className="py-4">1137</td>
                  <td className="py-4">0.027</td>
                  <td className="py-4">10X</td>
                  <td className="py-4">Exclusive IDO</td>
                  <td className="py-4">Ethereum</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-center gap-2 mt-8">
            <button className="px-2 py-1 text-lg">&lt;</button>
            <button className="px-3 py-1 bg-white text-black rounded-sm">1</button>
            <button className="px-3 py-1">2</button>
            <button className="px-2 py-1 text-lg">&gt;</button>
          </div>
        </div>
      </section>
    </div>
  )
}

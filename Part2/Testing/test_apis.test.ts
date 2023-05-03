import { spawnSync } from 'child_process';
import { expect, test } from '@jest/globals';

// RUN WITH: npx jest test_apis.test.ts

// POST package sucess output
test('post package, success', () => {
  const delete_command = 'bash test12delete.sh';
  const delete_process = spawnSync(delete_command, { shell: true });

  const curlCommand = 'bash test1package.sh'
  const expectedJson = {"metadata": {"Name": "fecha", "Version": "4.2.3", "ID": "fecha_4.2.3"}, "data": {"Content": "UEsDBBQAAAAIAGqTllalf4NQWAAAAIMAAAAOAAAAZmVjaGEvLmJhYmVscmOr5lIAAqWCotTi1JJiJSuFaLCAApwGSjokJSal5uhD1Oim5pUpQeViwXSsDtSMnNL0zDywGXAtYCHdgqL8gvzixBzd/IKSzPw8ICM5IzEzLzMvXSmWqxYAUEsDBBQAAAAAAGqTllZOXoENCAAAAAgAAAAVAAAAZmVjaGEvLmJyb3dzZXJzbGlzdHJjZGVmYXVsdHNQSwMEFAAAAAgAapOWVu+VbyuDAAAAtwAAABMAAABmZWNoYS8uZWRpdG9yY29uZmlnRY3NCsIwEITveYqB3oRevOckPoInkRDMpi7E3ZKs1vr0/tTicT5m5utgOvZXbYZ9YtO6U8k8IHMhV1UNHlZv5FyHg/CjbzYXgtBUWKhhYrsgrhkkiWUA3anOy8dxc3JvGjSHb8OjZMfSqFrILLGEdfsTsSQSC4vHo43x/If8/LCtewFQSwMEFAAAAAgAapOWVt8Ln1igAAAAUQEAABIAAABmZWNoYS8uZXNsaW50cmMuanOVkMEKwjAMhu97itDLLlbvFcH3EA+6ZaOwNSXNYDL27sZW8NKLl5bwfU3+dKZ+mfCIaySWBBfYGgAmEgfCCx60ig9OyA7aq7wipo59FItp8kFOhbVZm5bRh+TgpgXU7KzdPweugqH/uYU7xo7mWQn22VVSurrK6HLZv97UZEYR/90hh2P9EI22ZW4qXZ6PYCVZPwZiNA4MDYNRe2/2c/MGUEsDBBQAAAAAAGqTllZqXiJ7KAAAACgAAAAQAAAAZmVjaGEvLmdpdGlnbm9yZW5vZGVfbW9kdWxlcwpjb3ZlcmFnZQoubnljX291dHB1dAp0cy1vdXRQSwMEFAAAAAAAapOWViewnkk2AAAANgAAAAwAAABmZWNoYS8ubnljcmN7CiAgICAiZXh0ZW5kcyI6ICJAaXN0YW5idWxqcy9ueWMtY29uZmlnLXR5cGVzY3JpcHQiCn1QSwMEFAAAAAgAapOWVrCasnUhAAAAJQAAABEAAABmZWNoYS8udHJhdmlzLnltbMtJzEsvTUxPtVLIy09Jjc8q5oLSVlwKCroKhkZ6hiZcAFBLAwQUAAAACABqk5ZWNI9TxHABAAD3AgAAEAAAAGZlY2hhL2Jvd2VyLmpzb25dUstuwjAQvPMVUY6ocV6VWnHm0B5641YVtCRLYogfsh1QhPj3Ok5s0t68M2PP7HrvqyiKOTCMN1F8wqqF+GWEGFAeIHLWE3pFpalwREFKUkxoKxhKaNwTrTFSb9K0oabtj6QSLDUwdEK1cEGdLhygN61Q2l76tqUFdk4XfYzC2EI/TlajrhSVZrbdgsHoJBQDYyhvIuB1JMGm4s0cXNR9h7tB4vNlYLUj7bHpxBE67Usuanx6XXC4CVUvMtXWzmtHm1Aw2zM3vpoChSo0Gagx69OnoxVy7eb19bmbctOGC7XIvF6nZL2MeZg6C9GP4obqYAcsBbdRAm5Qm+X5zyyvW5TIa+QVxbHN+6S7gA05xtlnJLc/m/sHzqAZ5ZhUU7Z4X5CclJ5115JZM18vyetfWrbAjWBnnXTQ86pF5Y3+Kyth92veI8sX5C38Wt9Jh5bkneTZEk76pqOnwbE5yead9KRCv9uWLEg2zuKxeqx+AVBLAwQUAAAACABqk5ZWNHfmEdsDAADsBwAAEgAAAGZlY2hhL0NIQU5HRUxPRy5tZIVVTW/bRhC981dMoYNsQaYl2UGjGgFax3WQAnIM2C2QFAW4IlciLXKX2F1KVQz/97zZJalaPtQHk+LOx5t5M28HgwFdxrP4Ijqj2+JfmdGyWdOucDn9+fiRMuEkaYXnvizWubNkxbZQa0uuqCQN5pdRNGhDTPsQVWEtjMjqxqSSKlH3R1amjSncnvbT9+rgO4l+yzIcF1bfcEqh+vdHTlQJu7Gd+bQ3/0YrbSrhzmthbPBa+TT30jQe4netJCLZRgJCcEq+Ja0bOb2RKqYHKclIkSERDqjSBj5qpWO6LtbkcqE2KFjTrytpZrOVN9qhCq7R5ZJSncm4L1GQdUaodZuXdrlUAVCa8+esB2aRhabz+SRAGPz8nrhGlDhBiaPRQjwh060UrjEw5vLoGkA3nDgE8yFcXljaSmMLrUYj36YBfa5qo7eykspZYBv9JcoiC4RytxBiRGd0vadMrkRTOlpJhAT1ZYnYMt3Qlj2YK73yfjameyO3hW5suadkNpnOz969O5tMEwLM8HsyPbucJbTTTZlRYCXVxsjUlfsxISvm4Q+xFTY1Re0oFYpQR1aiWS6mO71DPdseqQ1wjEQDFCWqKcsEBtaBLK7p9wda6KwpA/WPBk18yEN7Hpq61sZxjV914xMpjl7x17bWxAMM6MNEcPRM1hL/FBBHSZI82ah1eg4241DXC62MrmjoQw2voiicnsRxfHoVeRP/zjFaSo65QwkBAs95giHfH5XqR6c+9Dyc+hlLvE8YnOI/VJNY4nWMNXb/30p0BBg+ejQ84Dk6hIeVLmxc2EPe1APxr3sSGnncCX6J2Y8+0DOhC/TSfvRh42q/wBOHw5sbGtNiMaav+BtSaNad3B113ndpTB0BAPip1EtRchM+I8/RJ45u3xD0xuvkOSL8nZ8zxOjlNHobxJsEuL8co4XHVc8uXWBpj1SU2Wu8Ei6NSDcS7ARGw/4FXnrnWe/c6wZ0yJoUmlby+uOX0sxqWjYsZP1isQaoujrgmCDUAmOQMZtYksovie25zl6NRuhTshIlLwM8wnSEcLgaUNbR1bCXwtB8Pvd4cn8jUImd5Od3afTBddYqtdvXst156E2hIJ5aeVG9u18czDthh4IWqes0rROgsHiGFdm1k2yJsfIV9XrYT3iZGqjPUSR0antx2iXki6cT7Z6xjp0b3V0TgafIu3Bzb/3Qs5y43OidJWmMNvYtCmRLwtx38hIuthYVSsG2YlF3eZcFMkgiTWXtoLY3/kvVWAdQ1lLyZfkEwmNsu9Pc0djpB0RS6zgVZXnCEWBySj99wGr9rb21j/LPMImjH1BLAwQUAAAACABqk5ZWD6jhmyECAABqBAAAFQAAAGZlY2hhL0NPTlRSSUJVVElORy5tZKVUO4/bMAze/SsIZOgDabLf1qY44Ia+gXYoCoSW6ViILbkUdYb/fUkpCXDFbTea9Ed+D9obOMQg7NssPpyaXwTIBHGmABK3gKGDE6NQn0foI1tlBXeDxJBgwo6gXUEG0s405eBl3TXNZgPfaY5sg+EhpUypzHufzlb5ps9lQPOBdHJdag0M4O3tLcwjYSJIhOyGMv936YAwujPxn9eDyJzu9vuTlyG3O12/F1zHyAOeKe17cgPuCya9UUHK9azzsm5bY+a6BwZM4ZUAjkzYrdCSiufCnLqq4yM90hjniYI0zU+fvFQ2Dy9j03u1A2H0SSD21fXa1vEoEIi0L6Jr1Silch/5vLXVAdwYAxUWRvWuOR6Pje691J9hYoLf5UQccKLKZaftAlSNG/hMC9wTirqTmuZr9b5wuiYCi45TwjPHOSYsF6GPQYF9BYIWmHp0EtmybGu0SbCeQQyF8qI6dqDH1kVzfsEgFoh5smCSSzrUK1iSgXRnHkcd/deuprqz2JwbXKHoHM1SE/uR28lL2XkYMJxM0lv4UtQUwlWQDy8OcqdzLZdbFlY46CmpjKfetIxB77hVXzvNuy+I42SC+XjpGvjT7UhRNYsKTjBjql+PYrh+pCHq5YQikZgjJ8NW3f/5tbVMFBZc/b7W65XZm12neSdS9DVz4dXsPBPNNYgn3vfRZROg1iWn51FY4WP0VnJj7mxHDkyjOtCVP4IXnf4PUEsDBBQAAAAIAGqTllZp8S40fQIAADgEAAANAAAAZmVjaGEvTElDRU5TRV1SS4/aMBC++1eMOO1K0fYh9dKbCWZjNSSRY5ZyNIkhbkOMYlPEv+9MYHe7lZDQjGe+10R3FlZSQ+4aOwQLD1g8Mpb603V0hy7CQ/MIXz9/+QbaXHs/QmZ+28BYZcejC8H5AVyAzo52d4XDaIZo2wT2o7Xg99B0ZjzYBKIHM1zhZMeAC34XjRvccAADDRIxnIwdwgS/jxczWhxuwYTgG2cQD1rfnI92iCYS3971NsBDROWz+r4xe5xIWmt65gagt9cnuLjY+XOE0YY4uoYwEnBD059b0vD63LujuzPQ+uQ+MAQ9B3RAOhM4+tbt6d9Otk7nXe9Cl0DrCHp3jtgM1JzCTMjHJ8ws2L5niOBQ9+T1Xd00Q9JPFGi8RxSoc+n88aMTF9j+PA5Iaaed1mNkE+Mv20Tq0Pje972/kLXGD60jR+E7YxqfzM7/sZOX23EHH1HqTQId4PR+1ftT6Ezfw87eA0NejNf8Y2ck+hDx8M70cPLjxPe/zSfkzwTU5VJvuBIga6hU+SIXYgEzXmM9S2AjdVauNeCE4oXeQrkEXmzhhywWCYiflRJ1DaViclXlUmBPFmm+XsjiGea4V5T4HUv8gBFUl0CEdygpagJbCZVmWPK5zKXeJmwpdUGYy1IBh4orLdN1zhVUa1WVtUD6BcIWslgqZBErUegnZMUeiBcsoM54nhMV42tUr0gfpGW1VfI505CV+UJgcy5QGZ/n4kaFptKcy1UCC77iz2LaKhFFMRq7qYNNJqhFfBx/qZZlQTbSstAKywRdKv22upG1SIArWVMgS1WuEkZx4kY5geBeIW4oFDV8uAiOUL2uxRsgLATPEaumZbL4OozX/AtQSwMEFAAAAAgAapOWVnMHUbJoAgAA1QUAABIAAABmZWNoYS9wYWNrYWdlLmpzb26NVE1PHDEMvfMroj1wQJ0Mw7KlICFxAKk9lF5QL6hU2Yx3JpBJonxAV4j/3jiZr10V1FMUP/v52bHzekDIQrEOFhdksQHessUnND2DdUIrtJ7SE7rM1hoct8L4HrlmHshG2455L1RDmKqJYTFQNdm/YyI5SrEuEzkNXU0fXY/qOkjYxQcs53ERfI3XaPDgfKGV3KK/d4XSNRA0DiG9D8LGQhQElhQFb4E/kaPoRJzl5RH1jhweEnBSKB9x+OMJ2iKIdmU6YoMi6yBknQxbjiws8sTTgtHWg730GPeOihSLMm5/XN/8vrn9eWlsrJRj14jVUgZDCmR1OlgOHTOYyDs+EOSO7hXyYkVs9k4hi+j+lrqFupzw2m5nDdua1NtG+IE4WImW1nvjLsrSs63UtmVP4K6iVxvWlOtubu4fBSnGXE+wfdG2xqe5z7R1HIMhBT7/eOl0B8rvlTXcxlkbIZwhzPMr5WHBt9qi3rskiHxFRXk6pOCgXCrv+7e7bFuHZjYue6V+VF4pnAsw62YbZRvWwP8SDLvxfA0GVA2KC5hJuRLOM7UO8tGVcZwKrtVGNAW+T55yzPNQ0WNaDf24msAij2qZj8LI0OSdejih1Sk9/iAkvYX9h2/GE3BGT5b7wKBwmL7k+IVWk18sI4teRdWj1cRtl+Bcgo7pOT0bkRlTRavzqdK8D33E6nwiy0Bf77QqA/nqPc+P2rrrGRopNuk7eVjOy8i5ipiscMHgwo85q8/jV5N3v2/Nip5OQPzM+tTVjHVP15KexZhx5DZCwmyjkKKPq+P0jMosn/YjES52Ps86fQpvB38BUEsDBBQAAAAIAGqTllbvs31iWAgAAPAdAAAPAAAAZmVjaGEvUkVBRE1FLm1k7Vn7T+NIEv7df0XtorsQJg/b4emBjGY2x87NbgAprFYcQqITN8SDH1G7DZfZm/vbr6r8iLGdIWJuf7pDiH5/VV1dX3W12YI7OZsLuP7h+kPi+S5MtNBJfLM913oRO/2+VuLRi7szrxep+74WSz9Sc/Eg4z4v7MWP9++mSoSz+UkgYi1Ve+O1bcP41buf6ydJf8EVWsJdpAKhtRfegwhdWAgVU3373/YvH9o9GEsRatARKLnwxUwWE2hyae1dEs60F4XC9/QSojsIokCGuvc57hnG1tYWnF2MjdvbWyNcBOCFsRa+n1mi243Fo+RBmnglVMiNJVZAuG46jbt4wimveoxhzCKMYy2mvoSZL+L45Me0wX+7sVbeQrpZaxopVyrp/jg0AI71NHKXVKO6SitUnQ+P+/in1GZ51c5U9qoXa6oBzR0eT4cT74uE7bEX9thqP3/xFqhV+7g/JVluebbds375EFd7rUGl+1vSRnSqF+kpNYn469Y/7QNr8Pbl/helnBbn/ycLGovQWyS+IA9rEvV9Iv5uHYYwSRaLSOn/zkawTN0LK+R7Q/Jc+C2W4Gl24q2S7YzblEe3IGYzudAxCOBdR9PPcqZhO1KgvUAiZ4JFm11IALk20Y5Xcp+SOlEhLc5oiY6fzurBREqYSj96ojFDPArPZ5pky3X0IEMi6lmkpQOFPk8eklTPFa4TIUilUJOnuQwxCMQxwnvhI/Kdg4YIJIaimFj6OTa8gGwJf+QCvsKdigJoMZNbbw1DLxeF9BPYpkjk8KY7We87J1O+Ax4eDzbplCaSLRa34WRI44jU78NPSawRPV0YG2m5HconRty2TWuvA5bZAdtsd6Dl4g+M8QdGUQeu8KfVfguI0zpVniuWcBY9ymAqFc7Xc1pl7bVqqNbR0WEHEHiA2FjYg1TGYI+FEGx3PO6ORjCfO0HgxHFvMpnA+1wWre+a+11zAObAsQeOZfZwLVyMW7ypM7SoCxjhH17ekRdH1J9D03DXsrq2WVe7uhSFeElQXo27x7F12y6v573b2CrpcImOWtfjErdo2o5pdc09x1yrlp0ik1ELBeM5elIZFREGZmqjXz30OeE3Gci0GA6h9jtwkNYJ7joKb4DPpUtHBNdC38DHj3hCOX4U4oGgnl0CAfRPc98xD1rF/bOVB1fjlu5CWaNtRs2XeVoieYWisI6iYBg7Z+eXf9tBlmbSNyXpc01wUuDF8aqnB1dRAuPfJpcQL+TMu1sWkaRXZTVLXkPqdCzj9ESrFY9TsG/y+nyR5hDMbzLPv8LE9xtZznK2W6dyqhKhljBQLvvsbgtPuYndZV/bRUdDJ2vnKJbZteyuZYK161iWY9ktpnBGYHYPJHADELqpZaVey6BUt9s1Amdi9vqD/tFhK/fqEusqYWW3rFwRjnZpg+Yerfej8L5pOY2n6uwW69fTsJG2L1Cd93b+iH7muZLPMJezC9gRzXQyVZKq1tHhgA+DGnwiWPKBdOAPvCSDKNRzslLswDVfny0ZShW1OmnjDo+21AyE+lI0xFR5/mpkWQx8TkKv1PBXDXEfoQPlrRgZ66FZlcx7Ms3zZhg9Ph93vVnWge0b42vt4A7RREds+FWo8EqpRYVFsdQ/+9FU+LScSFDjU3/HGMk7kfga0hQlY4lB1sOLim03IU9CA7YmScjWjri4TCQVv0uXW/NEUYkXHBUToVs3nRJIth6bGURWQ5Q4qyJSWDQIL6+nl2YGmyiqM/bqeAsVPwnWDTnLYgTr9H6h0hZjfEp38SnxeSy5Z2C5oOJ8pqlAPlAxkrOqoEwGxYNMjsrrKGw2z8R5/nOBMpO4zERioMmkaiZeJjvKqjkfMyXSOmsigouAdBABjS2CtBe9ZARejDFaksHpcURVVrtTPJyKeyHGl4WeU2D2vQfZ6/WAYhsFbMvSc8QbRachRtfl+d2YINpMJsjWw2oA3sA1tDTvOt1RyM6g3BbcXJcn/gVZDkMYwDswwYESOHRr8344OcGiDTu1kZu3qMhX46ux0zeMmntv/99rO//jXuus1m2PKn47esFdRzUvHaFzjqo+OXruim0Mo6tonKUQ6c085pu58b3SgWfeyzNr6U4pOt/z1OyuZzdPBxx+bAAnIyO++la5BNm4yAJw4rg/6tPVSK5R5OQOpzIwyhIZGsxvfifPckpjd5gsZWP0yOlAbUaRTeOUNOtdCSx35xqStEo/PWNaGckpLVOS0ljBNyFZwKjbjqkfLKleAkKt+mPc9giNyQeFaNkTueF5sJsn85xnUYLD+XyKWjyqMH0znd09nNQ39/G3VfpstPpYdcnJ9J/+4YjFVDvPE71INvxwxLG16YvEuPaFCGwg0lkW5p+bfPWoAtYQ8e1jfi9mDRTDHGB8Y1h6Z2Igeh1wEzI/A4r3QCYizZzzgLeJMPrkxOFurfVH66w/MGFgbSKjChjVEGMNNj4WU1S8YAfY8xrkmq6rc91Y28Iiv0v50GQQtyYELBaxB/ubCKjCuTVAvObpPBgUr27AS/t1wE3IdL2l2UOOT9U8L9hEznR4JYVqMs3VVbXnwISD1Dr2EZ7BJvA1zDqqdYS4+CdDNhHbNjdDnw7fj/sX4ybt39c6xnAx3gS0sk7UOgJYBJsATYcfo6TRtB/XeZ1tgz3YBLsKWEc0wfw+zHntoL4zUs9riK+I1Hi1eGGiZZNZgxp+TuZD2DvaBL0KWEcszLox5nQ4kTPkaJPGtf+XfK/GcR3xNRqfKpH9TwzWKz9Zp/whbCSmCrcW7wgBX4e4HpIxNwKdDimN/BKFjT73j2pHVgXomgcOGr9LH2FNFvomrb7hgXzJRho0Sv6m6FTySnAq9xtij2v/+PkPUEsDBBQAAAAIAGqTllakSM09QAEAAI0DAAAWAAAAZmVjaGEvcm9sbHVwLmNvbmZpZy5qc61RPU/DMBDd8ytOmVopbXc6IiEW+ANVhzS+lEO2z/KHQoX475xjq1nKAGWwZPl93LtnMo59hHTWNF5g9Gyg9ax1chun05nspkDtvqFCjReHYfDk4k36Ai+SwMkP+NK7cFNSYCOwSBr8mDUKxz7pCIcGYLeDRzbOYwioYDWyB0UehwgD25CMi8QWyMLJ8xTQr4tm8hQjWogs9CBxWSv0HRiyNBKqrdA+5YBIXYoP0AY/7EYc3vptDG03Q5zijBXi7PvME1CEibSGE0IOnHNJhIms4qkybW9QPGe/agaSwZs+j0pGLY+kMzOHrOMl4vY9XAmlkyCcbKra+fmroKVEwQ5L9at1V78035b6V+tjU4Wyx5P0+MpKRlsupVy6um8uU9Mp1/yXkn69usyqngLet/l1w39OjcH8nPr+xM1x33wDUEsDBBQAAAAIAGqTllYPTm2ZkgAAAAEBAAATAAAAZmVjaGEvdHNjb25maWcuanNvbmXOsQrDIBAG4D1PERwlJXu3QpcOpQ9QOli1cOX05NQhhLx71RQq1O38/uO/dRjLE5pcALR8CwnIR3Ec1wYNHZmMtvzVmCP/jmL6qaeLCwga0skvJZQ4244jZdb2qkKhl8LYm7EaFata+b/Y4Rm4tiM8+2LK6QspHsowi2bbHhHgNWZTz75317CepZzlHn1Mw/YBUEsBAhQAFAAAAAgAapOWVqV/g1BYAAAAgwAAAA4AAAAAAAAAAQAAAAAAAAAAAGZlY2hhLy5iYWJlbHJjUEsBAhQAFAAAAAAAapOWVk5egQ0IAAAACAAAABUAAAAAAAAAAQAAAAAAhAAAAGZlY2hhLy5icm93c2Vyc2xpc3RyY1BLAQIUABQAAAAIAGqTllbvlW8rgwAAALcAAAATAAAAAAAAAAEAAAAAAL8AAABmZWNoYS8uZWRpdG9yY29uZmlnUEsBAhQAFAAAAAgAapOWVt8Ln1igAAAAUQEAABIAAAAAAAAAAQAAAAAAcwEAAGZlY2hhLy5lc2xpbnRyYy5qc1BLAQIUABQAAAAAAGqTllZqXiJ7KAAAACgAAAAQAAAAAAAAAAEAAAAAAEMCAABmZWNoYS8uZ2l0aWdub3JlUEsBAhQAFAAAAAAAapOWViewnkk2AAAANgAAAAwAAAAAAAAAAQAAAAAAmQIAAGZlY2hhLy5ueWNyY1BLAQIUABQAAAAIAGqTllawmrJ1IQAAACUAAAARAAAAAAAAAAEAAAAAAPkCAABmZWNoYS8udHJhdmlzLnltbFBLAQIUABQAAAAIAGqTllY0j1PEcAEAAPcCAAAQAAAAAAAAAAEAAAAAAEkDAABmZWNoYS9ib3dlci5qc29uUEsBAhQAFAAAAAgAapOWVjR35hHbAwAA7AcAABIAAAAAAAAAAQAAAAAA5wQAAGZlY2hhL0NIQU5HRUxPRy5tZFBLAQIUABQAAAAIAGqTllYPqOGbIQIAAGoEAAAVAAAAAAAAAAEAAAAAAPIIAABmZWNoYS9DT05UUklCVVRJTkcubWRQSwECFAAUAAAACABqk5ZWafEuNH0CAAA4BAAADQAAAAAAAAABAAAAAABGCwAAZmVjaGEvTElDRU5TRVBLAQIUABQAAAAIAGqTllZzB1GyaAIAANUFAAASAAAAAAAAAAEAAAAAAO4NAABmZWNoYS9wYWNrYWdlLmpzb25QSwECFAAUAAAACABqk5ZW77N9YlgIAADwHQAADwAAAAAAAAABAAAAAACGEAAAZmVjaGEvUkVBRE1FLm1kUEsBAhQAFAAAAAgAapOWVqRIzT1AAQAAjQMAABYAAAAAAAAAAQAAAAAACxkAAGZlY2hhL3JvbGx1cC5jb25maWcuanNQSwECFAAUAAAACABqk5ZWD05tmZIAAAABAQAAEwAAAAAAAAABAAAAAAB/GgAAZmVjaGEvdHNjb25maWcuanNvblBLBQYAAAAADwAPALUDAABCGwAAAAA=", "URL": "None", "JSProgram": "if (process.argv.length === 7) {\nconsole.log('Success')\nprocess.exit(0)\n} else {\nconsole.log('Failed')\nprocess.exit(1)\n}\n"}};
  const process = spawnSync(curlCommand, { shell: true });
  const output = process.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

//  POST package error for no authentication
// test('post package no auth', () => {
//   const curlCommand = 'bash test11package.sh'
//   const expectedJson = {"message": "Authentication failed."};
//   const process = spawnSync(curlCommand, { shell: true });
//   const output = process.stdout?.toString();
//   const response = JSON.parse(output || '');
//   expect(response).toEqual(expectedJson);
// });

//  POST package error message for missing fields
test('post package, missing fields', () => {
  //const curlCommand1 = 'bash test1package.sh'
  const curlCommand2 = 'bash test16package.sh'
  const expectedJson = {"message": "There is missing field(s) in the PackageData/AuthenticationToken or it is formed improperly (e.g. Content and URL are both set), or the AuthenticationToken is invalid."}
  //const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

// INCLUDE MISSING FIELDS ERROR WHEN I CAN RUN PACKAGE

test('delete reset, success', () => {

  const curlCommand = 'bash test2reset.sh'
  //const expectedJson = { message: 'Success.' };
  const process = spawnSync(curlCommand, { shell: true });
  const output = process.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual("Registry is reset.");
});

// checks for error message when reset is requested
// test('delete reset, no permission', () => {

//   const curlCommand = 'bash test3reset.sh'
//   const expectedJson = {"message": "You do not have permission to reset the registry."}
//   const process = spawnSync(curlCommand, { shell: true });
//   const output = process.stdout?.toString();
//   const response = JSON.parse(output || '');
//   expect(response).toEqual(expectedJson);
// });

//  checks for correct output when regex found
test('post regex, regex found', () => {
  const curlCommand1 = 'bash test1package.sh'
  const curlCommand2 = 'bash test4regex.sh'
  const expectedJson = [ { Version: '4.2.3', Name: 'fecha' } ];
  const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

//  checks for error message when regex yield no package in set
test('post regex, regex not found', () => {
  //const curlCommand1 = 'bash test1package.sh'
  const curlCommand2 = 'bash test5regex.sh'
  const expectedJson = { "message": "Package does not exist." };
  //const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

//checks for missing field error message in post regex
test('post regex, missing fields', () => {
  //const curlCommand1 = 'bash test1package.sh'
  const curlCommand2 = 'bash test6regex.sh'
  const expectedJson = {"message": "There is missing field(s) in the PackageData/AuthenticationToken or it is formed improperly (e.g. Content and URL are both set), or the AuthenticationToken is invalid."}
  //const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

//  checks for correct id
test('get ID, ID exists', () => {
  //const curlCommand1 = 'bash test1package.sh'
  const curlCommand2 = 'bash test7id.sh'
  const expectedJson = {"data": {"Content": "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", "JSProgram": "if (process.argv.length === 7) {\nconsole.log('Success')\nprocess.exit(0)\n} else {\nconsole.log('Failed')\nprocess.exit(1)\n}\n", "URL": "None"}, "metadata": {"ID": "fecha_4.2.3", "Name": "fecha", "Version": "4.2.3"}};
  //const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

//  checks for correct output when id doesnt exist
test('get ID, ID does not exists', () => {
  //const curlCommand1 = 'bash test1package.sh'
  const curlCommand2 = 'bash test8id.sh'
  const expectedJson = {"message": "Package does not exist."};
  //const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

//  checks for default put authentication output
test('put authenticate', () => {
  const curlCommand = 'bash test10auth.sh'
  const expectedJson = {"message": "This system does not support authentication."};
  const process = spawnSync(curlCommand, { shell: true });
  const output = process.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

//  correct output for deleting a package
test('delete package id, success', () => {
  //const curlCommand1 = 'bash test1package.sh'
  const curlCommand2 = 'bash test12delete.sh'
  const expectedJson = {"message": "Package is deleted."};
  //const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

//  checks for error message when user requests to delete a package that isnt in database
test('delete package id, DNE', () => {
  //const curlCommand1 = 'bash test12delete.sh'
  const curlCommand2 = 'bash test12delete.sh'
  const expectedJson = {"message": "Package does not exist."};
  //const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

//  checks for error message when there is no authentication
// test('delete package id, no auth', () => {
//   const curlCommand1 = 'bash test1package.sh'
//   const curlCommand2 = 'bash test13delete.sh'
//   const expectedJson = {"message": "Authentication failed."};
//   const process1 = spawnSync(curlCommand1, { shell: true });
//   const process2 = spawnSync(curlCommand2, { shell: true });
//   const output = process2.stdout?.toString();
//   const response = JSON.parse(output || '');
//   expect(response).toEqual(expectedJson);
// });

//  when package and authentication is provided, rate is given
test('rate, success', () => {
  const curlCommand1 = 'bash test1package.sh'
  const curlCommand2 = 'bash test14rate.sh'
  //const curlCommand3 = 'bash cat_json.sh'

  const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  //const process3 = spawnSync(curlCommand3, { shell: true });

  const output = process2.stdout?.toString();
  const dic = JSON.parse(output)

  //  checks each metric is there
  expect(dic).toHaveProperty("BusFactor")
  expect(dic).toHaveProperty("Correctness")
  expect(dic).toHaveProperty("RampUp")
  //expect(dic).toHaveProperty("ResponsiveMaintainer")
  expect(dic).toHaveProperty("Responsiveness")
  expect(dic).toHaveProperty("LicenseScore")
  expect(dic).toHaveProperty("GoodPinningPractice")
  expect(dic).toHaveProperty("RampUp")
  expect(dic).toHaveProperty("NetScore")
  expect(Object.keys(dic).length).toBe(8);
});

//  when user doesnt give authentication for rate
// test('rate, no authorization', () => {
//   const curlCommand1 = 'bash test1package.sh'
//   const curlCommand2 = 'bash test15rate.sh'
//   const curlCommand3 = 'bash cat_json.sh'

//   const process1 = spawnSync(curlCommand1, { shell: true });
//   const process2 = spawnSync(curlCommand2, { shell: true });
//   const process3 = spawnSync(curlCommand3, { shell: true });

//   const output = process3.stdout?.toString();
//   const response = JSON.parse(output || '');
//   const expectedJson = {"message": "Authentication failed."};
//   expect(response).toEqual(expectedJson);
// });

//  package requested is there
test('POST packages, success', () => {
  //const curlCommand1 = 'bash test1package.sh'
  const curlCommand2 = 'bash test17packages.sh'
  const expectedJson = [{"ID": "fecha_4.2.3", "Name": "fecha", "Version": "4.2.3"}];
  //const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

//  checks for appropriate response when there is no authentication provided
// test('POST packages, no authorization', () => {
//   const curlCommand1 = 'bash test1package.sh'
//   const curlCommand2 = 'bash test18packages.sh'
//   const expectedJson = {"message": "Authentication failed."}
//   const process1 = spawnSync(curlCommand1, { shell: true });
//   const process2 = spawnSync(curlCommand2, { shell: true });
//   const output = process2.stdout?.toString();
//   const response = JSON.parse(output || '');
//   expect(response).toEqual(expectedJson);
// });

//  checks for appropriate response when the package requested does not exist
test('POST packages, package DNE', () => {
  //const curlCommand1 = 'bash test1package.sh'
  const curlCommand2 = 'bash test19packages.sh'
  const expectedJson = {"message": "Package does not exist."}
  //const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

//  validates generated zipfiles
test('GET ID, Download', () => {
  const curlCommand = "bash clean.sh"
  //const curlCommand1 = 'bash test1package.sh'
  const curlCommand2 = 'bash test7id.sh'
  const curlCommand3 = 'diff package.zip ../Zip*/pack*'
  const process0 = spawnSync(curlCommand, { shell: true });
  //const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const process3 = spawnSync(curlCommand3, { shell: true });
  const output = process3.stdout?.toString();
  expect(output).toEqual("");
});


// checks for metric disqualified
test('POST package, metric disqualified', () => {
  const curlCommand1 = 'bash test22package.sh'
  const process = spawnSync(curlCommand1, { shell: true });
  const output = process.stdout?.toString();
  const response = JSON.parse(output || '');
  const expected = {message: 'Package is not uploaded due to the disqualified rating for nodist.'}
  expect(response).toEqual(expected);
});

// success in URL version
test('POST package, URL version success', () => {
  const curlCommand1 = 'bash test22package.sh'
  const process = spawnSync(curlCommand1, { shell: true });
  const output = process.stdout?.toString();
  const response = JSON.parse(output || '');
  const expectedJson = {"message": "There is missing field(s) in the PackageData/AuthenticationToken or it is formed improperly (e.g. Content and URL are both set), or the AuthenticationToken is invalid."}
  expect(response).not.toEqual(expectedJson);
});

test('POST package, metric choke', () => {
  const curlCommand1 = 'bash test23package.sh'
  const process = spawnSync(curlCommand1, { shell: true });
  const output = process.stdout?.toString();
  const response = JSON.parse(output || '');
  const expected = {"message":"Package is not uploaded due to the disqualified rating for Responsiveness."}
  expect(response).toEqual(expected);
});

